import base64
from datetime import datetime, timedelta
import io
import os
import re
import time
from uuid import UUID

from PIL import Image
import psycopg2

from database import db
from emails import *
from gazetteer import *
from localization import *
from logger import logger
import mask
from mlemail import *
from mlparse import *
from mlutils import *
from model import *
import search
import spam
from units import *
from utils import *

BASE_DIR = os.path.dirname(__file__)

MAX_MATCHES = 8
MAX_LENGTH = 1000

# JSON returns


def handle_closestnames(entry, values, files):
    if "query" not in values:
        return {"error": "No query specified."}

    MAX_MATCHES = 5

    query = values["query"].lstrip()

    closest = GazClosestMatchesQuick(query, MAX_MATCHES)

    return {"matches": closest}


def handle_mlaccount(entry, values, files):
    id = entry.id

    # TODO Find a mechanism for updating a member's email address too..
    attributes = ["password"]

    attrs = {}
    for attr, value in values.items():
        if not attr in attributes:
            continue
        if not value:
            continue
        if attr.endswith("_choice"):
            attrs[attr] = eval(value)
        elif isinstance(value, str):
            attrs[attr] = value[:MAX_LENGTH]
        else:
            attrs[attr] = value
    for attr in attributes:
        if attr in attrs:
            continue
        attrs[attr] = None

    db.session.query(ProfileModel).filter(ProfileModel.id == id).update(attrs)
    db.session.commit()

    return {"message": "Account updated successfully."}


def handle_mladdfavorite(entry, values, files):
    id = entry.id

    ids = [int(x) for x in values["id"].split("|")]

    for id_favorite in ids:
        item = FavoriteModel(id=id, id_favorite=id_favorite)
        db.session.add(item)
    db.session.commit()

    if len(ids) == 1:
        return {"message": "This member has been added to your favorites list."}
    else:
        return {"message": "These members have been added to your favorites list."}


def handle_mlblock(entry, values, files):
    id = entry.id

    ids = [int(x) for x in values["id"].split("|")]

    for id_block in ids:
        item = BlockedModel(id=id, id_block=id_block)
        db.session.add(item)
    db.session.commit()

    if len(ids) == 1:
        return {"message": "This member has now been blocked."}
    else:
        return {"message": "These members have now been blocked."}


def handle_mldeletefavorite(entry, values, files):
    id = entry.id

    if "ids" in values:
        ids = values["ids"]
    else:
        ids = [int(x) for x in values["id"].split("|")]

    for id_favorite in ids:
        db.session.query(FavoriteModel).filter(
            FavoriteModel.id == id, FavoriteModel.id_favorite == id_favorite
        ).delete()
    db.session.commit()

    if len(ids) == 1:
        return {"message": "This member has been removed from your favorites list."}
    else:
        return {"message": "These members have been removed from your favorites list."}


def handle_mldeletephoto(entry, values, files):
    id = entry.id

    if "pids" in values:
        pids = values["pids"]
    else:
        pids = [int(x) for x in values["pid"].split("|")]

    for pid in pids:
        # Ensure this member owns the photo first
        entry = db.session.query(EmailModel.id).filter(PhotoModel.pid == pid).one_or_none()
        if not entry:
            return {"error": "Photo %d not found." % (pid)}
        if entry.id != id:
            return {"error": "You are not the owner of photo %d." % (pid)}

    DeletePhotos(db.session, pids)

    deleted = pids

    pids = []
    master = 0
    entries = db.session.query(PhotoModel.pid, PhotoModel.master).filter(PhotoModel.profile_id == id).all()
    for entry in entries:
        pids.append(entry.pid)
        if entry.master:
            master = entry.pid

    if len(deleted) == 1:
        return {"message": "This photo has been deleted.", "pids": pids, "master": master}
    else:
        return {"message": "These photos have been deleted.", "pids": pids, "master": master}


def handle_mlmasterphoto(entry, values, files):
    if "pid" not in values:
        return {"error": "No Photo selected."}

    id = entry.id

    pid = int(values["pid"])

    # Ensure this member owns the photo first
    entry = db.session.query(EmailModel.id).filter(PhotoModel.pid == pid).one_or_none()
    if entry.id != id:
        return {"error": "You are not the owner of this photo."}
    # Remove the master flag from all photos
    db.session.query(EmailModel).filter(EmailModel.id == id).update({"master": False})
    # Restore the master flag for the selected photo
    db.session.query(EmailModel).filter(PhotoModel.pid == pid).update({"master": True})
    db.session.commit()

    pids = []
    master = 0
    entries = db.session.query(PhotoModel.pid, PhotoModel.master).filter(PhotoModel.profile_id == id).all()
    for entry in entries:
        pids.append(entry.pid)
        if entry.master:
            master = entry.pid

    return {"message": "This photo has been set to your main profile photo.", "pids": pids, "master": master}


def handle_mlprofile(entry, values, files):
    if "name" not in values:
        return {"error": "name not specified."}

    profile_id = entry.id

    values["height"] = ParseHeight(values.get("height"))

    attributes = [
        "name",
        "gender",
        "ethnicity",
        "height",
        "weight",
        "education",
        "status",
        "smoking",
        "drinking",
        "occupation",
        "summary",
        "description",
    ]

    attrs = {}
    location = values["location"]
    if location:
        tuple = GazLocation(location)
        if not tuple:
            return {"matches": GazClosestMatches(location, MAX_MATCHES)}
        attrs["location"] = location
        attrs["country"] = GazCountry(location)
        attrs["x"] = tuple[0]
        attrs["y"] = tuple[1]
        attrs["tz"] = tuple[2]
    for attr, value in values.items():
        if not attr in attributes:
            continue
        if not value:
            continue
        if attr.endswith("_choice"):
            attrs[attr] = eval(value)
        elif isinstance(value, str):
            attrs[attr] = value[:MAX_LENGTH]
        else:
            attrs[attr] = value
    for attr in attributes:
        if attr in attrs:
            continue
        attrs[attr] = None

    db.session.query(ProfileModel).filter(ProfileModel.id == profile_id).update(attrs)
    db.session.commit()

    return {"message": "Profile updated successfully."}


def handle_mlregister(entry, values, files):
    if "email" not in values:
        return {"error": "No Email Address specified."}
    if "password" not in values:
        return {"error": "password not specified"}
    if "dob" not in values:
        return {"error": "No Date of Birth specified."}
    if "name" not in values:
        return {"error": "No Display Name specified."}
    if "gender" not in values:
        return {"error": "No Gender specified."}
    if "ethnicity" not in values:
        return {"error": "No Ethnicity specified."}
    if "gender_choice" not in values:
        return {"error": "No Seeking gender specified."}
    if "location" not in values:
        return {"error": "No Location specified."}

    email = values["email"].lower()
    dob = values["dob"]
    location = values["location"]

    if not ParseEmail(email):
        return {"error": "Email Address not valid."}
    dt = ParseDob(dob)
    if not dt or dt.year < 1900:
        return {"error": "Date of birth not valid."}
    age = Age(dt)
    if age < 18:
        return {"error": "Sorry, you're too young to register."}

    entry = db.session.query(ProfileModel).filter(ProfileModel.email == email).one_or_none()
    if entry:
        return {"error": "Email Address already in use."}

    now = datetime.utcnow()

    attrs = {}
    attrs["created2"] = now
    attrs["dob"] = dt.strftime("%Y-%m-%d")
    location = values["location"]
    if location:
        tuple = GazLocation(location)
        if not tuple:
            return {"matches": GazClosestMatches(location, MAX_MATCHES)}
        attrs["location"] = location
        attrs["country"] = GazCountry(location)
        attrs["x"] = tuple[0]
        attrs["y"] = tuple[1]
        attrs["tz"] = tuple[2]
    for attr, value in values.items():
        if attr.endswith("_choice"):
            attrs[attr] = eval(value)
        elif isinstance(value, str):
            attrs[attr] = value[:MAX_LENGTH]
        else:
            attrs[attr] = value

    # Create a new profile entry
    item = ProfileModel(**attrs)
    db.session.add(item)
    db.session.commit()
    assert item.id

    profile_id = item.id

    # Create a uuid to use in the verification email
    uuid = UUIDModel(profile_id=profile_id, expiry=now + timedelta(minutes=15))
    db.session.add(uuid)
    db.session.commit()
    assert uuid.uuid

    EmailVerify(db.session, email, uuid.uuid)

    return {"code": 1002}


def handle_mlresend(entry, values, files):
    if "email" not in values:
        return {"error": "email not specified"}

    email = values["email"].lower()

    # Retrieve the newly created id
    entry = db.session.query(ProfileModel.id).filter(ProfileModel.email == email).one_or_none()
    if not entry:
        return {"error": "Account not found."}

    EmailVerify(db.session, email, entry.id)

    return {"message": "Verify Registration email has been resent..."}


def handle_mlforgotpassword(entry, values, files):
    if "email" not in values:
        return {"error": "email not specified"}

    email = values["email"].lower()

    # Retrieve the password
    entry = db.session.query(ProfileModel).filter(ProfileModel.email == email).one_or_none()
    if not entry:
        return {"error": "Email Address not found."}

    now = datetime.utcnow()

    profile_id = entry.id

    # Create a uuid to use in the verification email
    uuid = UUIDModel(profile_id=profile_id, expiry=now + timedelta(minutes=15))
    db.session.add(uuid)
    db.session.commit()
    assert uuid.uuid

    EmailResetPassword(db.session, email, uuid)

    return {"message": "Your password reset email has been sent..."}


def handle_mlresetpassword(entry, values, files):
    if "uuid" not in values:
        return {"error": "uuid not specified"}
    if "email" not in values:
        return {"error": "email not specified"}
    if "password" not in values:
        return {"error": "password not specified"}

    uuid = values["uuid"]
    email = values["email"]
    password = values["password"]

    entry = db.session.query(UUIDModel.profile_id).filter(UUIDModel.uuid == UUID(uuid)).one_or_none()
    if not entry:
        return {"error": "This reset password link has expired."}

    profile_id = entry.profile_id

    db.session.query(ProfileModel).filter(ProfileModel.id == profile_id, ProfileModel.email == email).update(
        {"password": password}
    )
    db.session.commit()

    return {"message": "Your password has been changed..."}


def handle_mlchangepassword(entry, values, files):
    if "password" not in values:
        return {"error": "password not specified"}

    password = values["password"]

    profile_id = entry.id

    db.session.query(ProfileModel).filter(ProfileModel.id == profile_id).update({"password": password})
    db.session.commit()

    return {"message": "Your password has been changed..."}


def handle_mllocation(entry, values, files):
    if "location" not in values:
        return {"error": "No location specified."}

    location = values["location"].strip()

    tuple = GazLocation(location)
    if not tuple:
        return {"matches": GazClosestMatches(location, MAX_MATCHES)}

    return {"code": 1003}


def handle_mlseeking(entry, values, files):
    profile_id = entry.id

    if "gender_choice" not in values:
        return {"error": "gender_choice not specified."}

    values["age_min"] = ParseAge(values.get("age_min"))
    values["age_max"] = ParseAge(values.get("age_max"))
    values["age_min"], values["age_max"] = ParseRange(values["age_min"], values["age_max"])
    values["height_min"] = ParseHeight(values.get("height_min"))
    values["height_max"] = ParseHeight(values.get("height_max"))
    values["height_min"], values["height_max"] = ParseRange(values["height_min"], values["height_max"])

    attributes = [
        "gender_choice",
        "ethnicity_choice",
        "age_min",
        "age_max",
        "height_min",
        "height_max",
        "weight_choice",
        "looking_for",
    ]

    attrs = {}
    for attr, value in values.items():
        if not attr in attributes:
            continue
        if not value:
            continue
        if attr.endswith("_choice"):
            attrs[attr] = eval(value)
        elif isinstance(value, str):
            attrs[attr] = value[:MAX_LENGTH]
        else:
            attrs[attr] = value
    for attr in attributes:
        if attr in attrs:
            continue
        attrs[attr] = None

    db.session.query(ProfileModel).filter(ProfileModel.id == profile_id).update(attrs)
    db.session.commit()

    return {"message": "Seeking updated successfully."}


def handle_mlfilter(entry, values, files):
    profile_id = entry.id

    name = values.get("name")
    gender_choice = values.get("gender_choice")

    values["age_min"] = ParseAge(values.get("age_min"))
    values["age_max"] = ParseAge(values.get("age_max"))
    values["age_min"], values["age_max"] = ParseRange(values["age_min"], values["age_max"])
    values["height_min"] = ParseHeight(values.get("height_min"))
    values["height_max"] = ParseHeight(values.get("height_max"))
    values["height_min"], values["height_max"] = ParseRange(values["height_min"], values["height_max"])

    attributes = [
        "name",
        "sort",
        "location",
        "distance",
        "gender_choice",
        "age_min",
        "age_max",
        "ethnicity_choice",
        "height_min",
        "height_max",
        "weight_choice",
    ]

    attrs = {}
    location = values["location"]
    if location:
        tuple = GazLocation(location)
        if not tuple:
            return {"matches": GazClosestMatches(location, MAX_MATCHES)}
        attrs["location"] = location
        attrs["x"] = tuple[0]
        attrs["y"] = tuple[1]
        attrs["tz"] = tuple[2]
    for attr, value in values.items():
        if not attr in attributes:
            continue
        if not value:
            continue
        if attr.endswith("_choice"):
            attrs[attr] = eval(value)
        elif isinstance(value, str):
            attrs[attr] = value[:MAX_LENGTH]
        else:
            attrs[attr] = value
    for attr in attributes:
        if attr in attrs:
            continue
        attrs[attr] = None

    query = db.session.query(FilterModel).filter(FilterModel.profile_id == profile_id)
    if name:
        query = query.filter(FilterModel.name == name)
    else:
        query = query.filter(FilterModel.name.is_(None))
    filter = query.one_or_none()

    if filter:
        for attr, value in attrs.items():
            setattr(filter, attr, value)
    else:
        item = FilterModel(profile_id=profile_id, **attrs)
        db.session.add(item)
    db.session.commit()

    return {"code": 1000}


def handle_mlsendemail(entry, values, files):
    id = entry.id
    location = entry.location
    country = GazCountry(location)
    x = entry.x
    y = entry.y
    tz = entry.tz

    if "message" not in values:
        return {"error": "No message specified."}

    id_to = int(values["id"])
    message = values["message"]

    if Blocked(id_to, id):
        return {"error": "This member has blocked you."}

    if Blocked(id, id_to):
        return {"error": "You have blocked this member."}

    SetLocale(country)

    unit_distance, unit_height = Units(country)

    tuple = spam.AnalyseSpam(message)
    spammer = spam.AnalyseSpammer(id)
    if spam.IsSpamFactored(tuple, spammer, 3):
        with open(os.path.join(BASE_DIR, "junk-auto.log"), "a") as f:
            f.write("%d %s\n" % (id, re.sub("[\r\n]+", " ", message)))

    entry_to = db.session.query(ProfileModel).filter(ProfileModel.id == id_to).one_or_none()
    if not entry_to:
        return {"error": "This member cannot be found."}

    notifications = entry_to.notifications

    now = datetime.utcnow()

    item = EmailModel(id_from=id, id_to=id_to, message=message, sent=now)
    db.session.add(item)
    db.session.commit()

    if not notifications & NOT_NEW_MESSAGE:
        EmailNotify(db.session, entry_to, entry)

    d = {}
    d["sent"] = True
    d["message"] = message
    d["image"] = None
    d["time"] = Since(now, False)
    d["viewed"] = False

    return {"message": "Your message has been sent.", "entry": d}


def handle_mlsendphoto(entry, values, files):
    IMAGE_MAX_SIZE = 400

    id = entry.id
    location = entry.location
    country = GazCountry(location)
    x = entry.x
    y = entry.y
    tz = entry.tz

    id_to = int(values["id"])

    if Blocked(id_to, id):
        return {"error": "This member has blocked you."}

    SetLocale(country)

    unit_distance, unit_height = Units(country)

    try:
        im = Image.open(files["file"].stream)
    except:
        return {"error": "Unrecognized image format."}
    # Ensure it is no bigger than this
    im.thumbnail((IMAGE_MAX_SIZE, IMAGE_MAX_SIZE), Image.ANTIALIAS)
    data = io.StringIO()
    im.save(data, "JPEG")
    image = "data:image/jpg;base64," + base64.b64encode(data.getvalue())

    entry_to = db.session.query(ProfileModel).filter(ProfileModel.id == id_to).one_or_none()
    if not entry_to:
        return {"error": "This member cannot be found."}

    notifications = entry_to.notifications

    now = datetime.utcnow()

    item = EmailModel(id_from=id, id_to=id_to, image=image, sent=now)
    db.session.add(item)
    db.session.commit()

    if not notifications & NOT_NEW_MESSAGE:
        EmailNotify(db.session, entry_to, entry)

    d = {}
    d["sent"] = True
    d["message"] = None
    d["image"] = image
    d["time"] = Since(now, False)
    d["viewed"] = False

    return {"message": "Your photo has been sent.", "entry": d}


def handle_mlspam(entry, values, files):
    id = entry.id

    id_spam = int(values["id"])

    with open(os.path.join(BASE_DIR, "junk-reported.log"), "a") as f:
        entries = (
            db.session.query(EmailModel.message)
            .filter(EmailModel.id_from == id_spam, EmailModel.id_to == id)
            .distinct()
            .all()
        )
        for entry in entries:
            f.write("%d %s\n" % (id_spam, re.sub("[\r\n]+", " ", entry.message)))
        db.session.commit()

    return {"message": "Thank you for reporting this member..."}


def handle_mlunblock(entry, values, files):
    id = entry.id

    if "ids" in values:
        ids = values["ids"]
    else:
        ids = [int(x) for x in values["id"].split("|")]

    for id_block in ids:
        db.session.query(BlockedModel).filter(BlockedModel.id == id, BlockedModel.id_block == id_block).delete()
    db.session.commit()

    if len(ids) == 1:
        return {"message": "This member has now been unblocked."}
    else:
        return {"message": "These members have now been unblocked."}


def handle_mluploadphoto(entry, values, files):
    IMAGE_MIN_SIZE = 100
    IMAGE_MAX_SIZE = 600

    id = entry.id

    try:
        im = Image.open(files["file"].stream)
    except:
        return {"error": "Unrecognized image format."}
    # Ensure it is at least this big
    if im.size[0] < IMAGE_MIN_SIZE or im.size[1] < IMAGE_MIN_SIZE:
        return {
            "error": "Photo is too small. It needs to be at least %d by %d pixels." % (IMAGE_MIN_SIZE, IMAGE_MIN_SIZE)
        }
    # Ensure it is no bigger than this
    try:
        im.thumbnail((IMAGE_MAX_SIZE, IMAGE_MAX_SIZE), Image.ANTIALIAS)
    except:
        return {"error": "Unsupported image format."}

    # Add watermark to bottom-right corner
    if im.mode != "RGBA":
        try:
            im = im.convert("RGBA")
        except:
            return {"error": "Unsupported image format."}
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    mark = Image.open(os.path.join(BASE_DIR, "watermark.png"))
    layer.paste(mark, (im.size[0] - mark.size[0], im.size[1] - mark.size[1]))
    im = Image.composite(layer, im, layer)

    now = datetime.utcnow()

    item = PhotoModel(profile_id=id, created=now)
    db.session.add(item)
    db.session.commit()
    assert item.pid

    # Create a photo file using pid and copy data into it
    filename = os.path.join(BASE_DIR, "static", PhotoFilename(entry.pid))
    if os.path.isfile(filename):
        logger.error("Photo file %s already exists!" % (filename))
        os.remove(filename)

    # Save the modified photo
    im = im.convert("RGB")
    im.save(filename, "JPEG")

    EmailNewPhoto(db.session, filename, entry.pid, id)

    pids = []
    master = 0
    entries = db.session.query(PhotoModel.pid, PhotoModel.master).filter(PhotoModel.profile_id == id).all()
    for entry in entries:
        pids.append(entry.pid)
        if entry.master:
            master = entry.pid

    return {"message": "Photo uploaded successfully.", "pids": pids, "master": master}


def handle_mlwink(entry, values, files):
    id = entry.id
    location = entry.location
    country = GazCountry(location)
    x = entry.x
    y = entry.y
    tz = entry.tz

    id_to = int(values["id"])

    if Blocked(id_to, id):
        return {"error": "This member has blocked you."}

    SetLocale(country)

    unit_distance, unit_height = Units(country)

    entry_to = (
        db.session.query(ProfileModel).filter(ProfileModel.id == id_to, ProfileModel.verified.is_(True)).one_or_none()
    )
    if not entry_to:
        return {"error": "This member cannot be found."}

    notifications = entry_to.notifications

    message = "Wink!"

    now = datetime.utcnow()

    item = EmailModel(id_from=id, id_to=id_to, message=message, sent=now)
    db.session.add(item)
    db.session.commit()

    if not notifications & NOT_NEW_MESSAGE:
        EmailWink(db.session, entry_to, entry)

    return {"message": "Your Wink! has been sent."}
