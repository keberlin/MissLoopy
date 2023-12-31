from datetime import date, datetime
import json
from uuid import UUID

from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import and_, func

from database import db
from gazetteer import *
from localization import *
from logger import logger
import mask
from mllist import *
from mlparse import *
from mlutils import *
import search
import spam
from units import *
from utils import *

PER_PAGE = 20

DEFAULT_SORT = "distance"
DEFAULT_DISTANCE = 50  # km
LIMIT_AGE_MIN = 18
LIMIT_AGE_MAX = 99
LIMIT_HEIGHT_MIN = "any"
LIMIT_HEIGHT_MAX = "any"

# HTML Pages


def handle_index(entry, values):
    # Get most favorite male members
    entries = (
        db.session.query(FavoriteModel.id_favorite, func.count(FavoriteModel.id.distinct()))
        .filter(ProfileModel.gender == 1)
        .join(ProfileModel, FavoriteModel.id_favorite == ProfileModel.id)
        .group_by(FavoriteModel.id_favorite, FavoriteModel.id)
        .order_by(FavoriteModel.id)
        .limit(2)
        .all()
    )
    male = [entry.id_favorite for entry in entries]

    # Get most favorite female members
    entries = (
        db.session.query(FavoriteModel.id_favorite, func.count(FavoriteModel.id.distinct()))
        .filter(ProfileModel.gender == 2)
        .join(ProfileModel, FavoriteModel.id_favorite == ProfileModel.id)
        .group_by(FavoriteModel.id_favorite, FavoriteModel.id)
        .order_by(FavoriteModel.id)
        .limit(2)
        .all()
    )
    female = [entry.id_favorite for entry in entries]

    ids = [female[0], male[0], female[1], male[1]]

    entries = []
    for id in ids:
        entry = db.session.query(ProfileModel.name, ProfileModel.location).filter(ProfileModel.id == id).one()
        d = {}
        d["id"] = id
        d["image"] = PhotoFilename(MasterPhoto(db.session, id))
        filename = os.path.join(BASE_DIR, "static", d["image"])
        d["size"] = ImageDimensions(filename)
        d["name"] = entry.name
        d["country"] = GazCountry(entry.location)
        entries.append(d)

    dict = {}
    dict["entries"] = entries

    return dict


def handle_register(entry, values):
    dict = {}
    today = date.today()
    dict["dob_max"] = date(today.year - AGE_MIN, today.month, today.day)

    return dict


def handle_verify(entry, values):
    if "uuid" not in values:
        return {"error": "uuid not specified"}
    if "email" not in values:
        return {"error": "email not specified"}

    uuid = values["uuid"]
    email = values["email"].lower()

    entry = db.session.query(UUIDModel.profile_id).filter(UUIDModel.uuid == UUID(uuid)).one_or_none()
    if not entry:
        return {"error": "This verification link has expired"}

    profile_id = entry.profile_id

    entry = (
        db.session.query(ProfileModel).filter(ProfileModel.id == profile_id, ProfileModel.email == email).one_or_none()
    )
    if not entry:
        return {"error": "Profile not found"}

    now = datetime.now()
    db.session.query(ProfileModel).filter(ProfileModel.id == profile_id).update(
        {"created": now, "verified": True}, synchronize_session=False
    )
    db.session.commit()

    return {}


def handle_profile(entry, values):
    id = entry.id
    location = entry.location

    country = GazCountry(location)
    unit_distance, unit_height = Units(country)

    dict = {}
    dict["name"] = entry.name
    dict["location"] = entry.location
    dict["gender"] = entry.gender
    dict["ethnicity"] = entry.ethnicity
    dict["height"] = Height(entry.height, unit_height, 2) or ""
    dict["weight"] = entry.weight or 0
    dict["education"] = entry.education or 0
    dict["status"] = entry.status or 0
    dict["smoking"] = entry.smoking or 0
    dict["drinking"] = entry.drinking or 0
    dict["occupation"] = entry.occupation
    dict["summary"] = entry.summary
    dict["description"] = entry.description

    return dict


def handle_photos(entry, values):
    id = entry.id

    pids = []
    master = 0
    entries = db.session.query(PhotoModel.pid, PhotoModel.master).filter(PhotoModel.profile_id == id).all()
    for entry in entries:
        pids.append(entry.pid)
        if entry.master:
            master = entry.pid

    dict = {}
    dict["id"] = id
    dict["pids"] = json.dumps(pids)
    dict["master"] = master

    return dict


def handle_seeking(entry, values):
    id = entry.id
    location = entry.location

    country = GazCountry(location)
    unit_distance, unit_height = Units(country)

    dict = {}
    dict["limit_age_min"] = LIMIT_AGE_MIN
    dict["limit_age_max"] = LIMIT_AGE_MAX
    dict["default_age_min"] = LIMIT_AGE_MIN
    dict["default_age_max"] = LIMIT_AGE_MAX
    dict["default_height_min"] = LIMIT_HEIGHT_MIN
    dict["default_height_max"] = LIMIT_HEIGHT_MAX
    dict["gender_choice"] = entry.gender_choice or 0
    dict["ethnicity_choice"] = entry.ethnicity_choice or 0
    dict["weight_choice"] = entry.weight_choice or 0
    dict["age_min"] = entry.age_min
    dict["age_max"] = entry.age_max
    dict["height_min"] = Height(entry.height_min, unit_height, 2) or ""
    dict["height_max"] = Height(entry.height_max, unit_height, 2) or ""
    dict["looking_for"] = entry.looking_for

    return dict


def handle_matches(entry, values):
    page = int(values.get("page", 0))
    per_page = int(values.get("per_page", PER_PAGE))

    id = entry.id
    location = entry.location
    x = entry.x
    y = entry.y
    tz = entry.tz
    gender = entry.gender
    age = Age(entry.dob)
    ethnicity = entry.ethnicity
    height = entry.height
    weight = entry.weight
    gender_choice = entry.gender_choice
    age_min = entry.age_min
    age_max = entry.age_max
    ethnicity_choice = entry.ethnicity_choice
    height_min = entry.height_min
    height_max = entry.height_max
    weight_choice = entry.weight_choice

    distance = 300
    entries = search.search2(
        db.session,
        distance,
        "distance",
        id,
        x,
        y,
        tz,
        gender,
        age,
        ethnicity,
        height,
        weight,
        gender_choice,
        age_min,
        age_max,
        ethnicity_choice,
        height_min,
        height_max,
        weight_choice,
    )
    ids = [entry.id for entry in entries]

    SaveResults(id, ids)

    total = len(entries)
    entries = entries[page * per_page : (page + 1) * per_page]

    country = GazCountry(location)
    unit_distance, unit_height = Units(country)

    SetLocale(country)

    criteria = []
    if gender_choice:
        criteria.append("%s" % (GenderList(gender_choice)))
    if age_min or age_max:
        criteria.append("%s years old" % (Range(age_min, age_max)))
    if height_min or height_max:
        criteria.append("%s tall" % (Range(Height(height_min, unit_height, 2), Height(height_max, unit_height, 2))))
    if ethnicity_choice:
        criteria.append("%s" % (EthnicityList(ethnicity_choice)))

    dict = {}
    dict["action"] = "member"
    dict["type"] = "short"
    dict["criteria"] = ", ".join(criteria)
    dict["entries"] = ListMembers(db.session, entries, None, location, x, y, tz, unit_distance)
    dict["total"] = total
    dict["page"] = page
    dict["per_page"] = per_page

    return dict


def handle_filter(entry, values):
    name = values.get("name")

    profile_id = entry.id

    sort = (
        distance
    ) = location = gender_choice = age_min = age_max = ethnicity_choice = height_min = height_max = weight_choice = None

    query = db.session.query(FilterModel).filter(FilterModel.profile_id == profile_id)
    if name:
        query = query.filter(FilterModel.name == name)
    else:
        query = query.filter(FilterModel.name.is_(None))
    filter = query.one_or_none()
    if filter:
        sort = filter.sort
        distance = filter.distance
        location = filter.location
        gender_choice = filter.gender_choice
        age_min = filter.age_min
        age_max = filter.age_max
        ethnicity_choice = filter.ethnicity_choice
        height_min = filter.height_min
        height_max = filter.height_max
        weight_choice = filter.weight_choice

    if sort is None:
        sort = DEFAULT_SORT
    if distance is None:
        distance = DEFAULT_DISTANCE
    if gender_choice is None:
        gender_choice = entry.gender_choice
    if ethnicity_choice is None:
        ethnicity_choice = entry.ethnicity_choice
    if weight_choice is None:
        weight_choice = entry.weight_choice

    country = GazCountry(location or entry.location)
    unit_distance, unit_height = Units(country)

    dict = {}
    dict["limit_age_min"] = LIMIT_AGE_MIN
    dict["limit_age_max"] = LIMIT_AGE_MAX
    dict["default_age_min"] = entry.age_min or LIMIT_AGE_MIN
    dict["default_age_max"] = entry.age_max or LIMIT_AGE_MAX
    dict["default_location"] = entry.location
    dict["default_height_min"] = Height(entry.height_min, unit_height, 2) or LIMIT_HEIGHT_MIN
    dict["default_height_max"] = Height(entry.height_max, unit_height, 2) or LIMIT_HEIGHT_MAX
    dict["metric"] = unit_distance == UNIT_KM
    dict["sort"] = sort
    dict["distance"] = distance
    dict["location"] = location or ""
    dict["gender_choice"] = gender_choice
    dict["age_min"] = age_min
    dict["age_max"] = age_max
    dict["ethnicity_choice"] = ethnicity_choice
    dict["height_min"] = Height(height_min, unit_height, 2) or ""
    dict["height_max"] = Height(height_max, unit_height, 2) or ""
    dict["weight_choice"] = weight_choice

    return dict


def handle_results(entry, values):
    name = values.get("name")
    page = int(values.get("page", 0))
    per_page = int(values.get("per_page", PER_PAGE))

    profile_id = entry.id
    gender = entry.gender
    age = Age(entry.dob)
    ethnicity = entry.ethnicity
    height = entry.height
    weight = entry.weight

    sort = (
        distance
    ) = location = gender_choice = age_min = age_max = ethnicity_choice = height_min = height_max = weight_choice = None

    query = db.session.query(FilterModel).filter(FilterModel.profile_id == profile_id)
    if name:
        query = query.filter(FilterModel.name == name)
    else:
        query = query.filter(FilterModel.name.is_(None))
    filter = query.one_or_none()
    if filter:
        sort = filter.sort
        distance = filter.distance
        location = filter.location
        x = filter.x
        y = filter.y
        tz = filter.tz
        gender_choice = filter.gender_choice
        age_min = filter.age_min
        age_max = filter.age_max
        ethnicity_choice = filter.ethnicity_choice
        height_min = filter.height_min
        height_max = filter.height_max
        weight_choice = filter.weight_choice

    if sort is None:
        sort = DEFAULT_SORT
    if distance is None:
        distance = DEFAULT_DISTANCE
    if location is None:
        location = entry.location
        x = entry.x
        y = entry.y
        tz = entry.tz
    if gender_choice is None:
        gender_choice = entry.gender_choice
    if age_min is None:
        age_min = entry.age_min
    if age_max is None:
        age_max = entry.age_max
    if ethnicity_choice is None:
        ethnicity_choice = entry.ethnicity_choice
    if height_min is None:
        height_min = entry.height_min
    if height_max is None:
        height_max = entry.height_max
    if weight_choice is None:
        weight_choice = entry.weight_choice

    entries = search.search2(
        db.session,
        distance,
        sort,
        profile_id,
        x,
        y,
        tz,
        gender,
        age,
        ethnicity,
        height,
        weight,
        gender_choice,
        age_min,
        age_max,
        ethnicity_choice,
        height_min,
        height_max,
        weight_choice,
    )
    ids = [entry.id for entry in entries]

    SaveResults(profile_id, ids)

    total = len(entries)
    entries = entries[page * per_page : (page + 1) * per_page]

    country = GazCountry(location)
    unit_distance, unit_height = Units(country)

    SetLocale(country)

    criteria = []
    if gender_choice:
        criteria.append("%s" % (GenderList(gender_choice)))
    if age_min or age_max:
        criteria.append("%s years old" % (Range(age_min, age_max)))
    if height_min or height_max:
        criteria.append("%s tall" % (Range(Height(height_min, unit_height, 2), Height(height_max, unit_height, 2))))
    if ethnicity_choice:
        criteria.append("%s" % (EthnicityList(ethnicity_choice)))

    dict = {}
    dict["action"] = "member"
    dict["type"] = "short"
    dict["around"] = (
        Distance(distance, unit_distance) + " around " + GazPlacename(location, entry.location)
        if distance
        else "Worldwide"
    )
    dict["criteria"] = ", ".join(criteria)
    dict["entries"] = ListMembers(db.session, entries, None, location, x, y, tz, unit_distance)
    dict["nav"] = "search"
    dict["total"] = total
    dict["page"] = page
    dict["per_page"] = per_page

    return dict


def handle_member(entry, values):
    if "id" not in values:
        return {"error": "id not specified"}

    id_view = int(values["id"])

    if entry:
        id = entry.id
        location = entry.location
        country = GazCountry(location)
        x = entry.x
        y = entry.y
        tz = entry.tz
    else:
        id = x = y = None
        country = "United States"
        tz = "America/New_York"

    dict = {}
    dict["id"] = id_view
    prev, next = PreviousNextResult(id, id_view)
    dict["id_previous"] = prev
    dict["id_next"] = next

    entry = (
        db.session.query(ProfileModel).filter(ProfileModel.id == id_view, ProfileModel.verified.is_(True)).one_or_none()
    )
    if not entry:
        dict["error"] = "This member does not exist or has removed their account."
        return dict

    dict["name"] = mask.MaskEverything(entry.name)

    if Blocked(id_view, id):
        dict["error"] = "This member has blocked you."
        return dict

    unit_distance, unit_height = Units(country)

    SetLocale(country)

    location = entry.location

    master = MasterPhoto(db.session, id_view)
    image = PhotoFilename(master)
    entries = db.session.query(PhotoModel.pid).filter(PhotoModel.profile_id == id_view).all()
    pids = list(filter(lambda x: x != master, [entry2.pid for entry2 in entries]))
    images = [PhotoFilename(pid) for pid in pids]

    dict["mylat"] = y * 360.0 / CIRCUM_Y if y else None
    dict["mylng"] = x * 360.0 / CIRCUM_X if x else None
    # About me
    dict["gender"] = Gender(entry.gender)
    dict["age"] = Age(entry.dob)
    dict["starsign"] = Starsign(entry.dob)
    dict["ethnicity"] = Ethnicity(entry.ethnicity)
    dict["location"] = entry.location
    dict["country"] = GazCountry(entry.location)
    dict["lat"] = entry.y * 360.0 / CIRCUM_Y
    dict["lng"] = entry.x * 360.0 / CIRCUM_X
    dict["height"] = Height(entry.height, unit_height, 2) or ""
    dict["weight"] = Weight(entry.weight)
    dict["education"] = Education(entry.education)
    dict["status"] = Status(entry.status)
    dict["smoking"] = Smoking(entry.smoking)
    dict["drinking"] = Drinking(entry.drinking)
    dict["summary"] = mask.MaskEverything(entry.summary)
    dict["occupation"] = mask.MaskEverything(entry.occupation)
    dict["description"] = mask.MaskEverything(entry.description)
    dict["last_login"] = Since(entry.last_login)
    dict["login_country"] = entry.last_ip_country
    dict["created"] = Datetime(entry.created, tz).strftime("%x")
    # Seeking
    dict["gender_choice"] = GenderList(entry.gender_choice)
    dict["age_range"] = Range(entry.age_min, entry.age_max)
    dict["looking_for"] = mask.MaskEverything(entry.looking_for)
    # Photos
    dict["image"] = image
    dict["images"] = images

    return dict


def handle_emailthread(entry, values):
    if "id" not in values:
        return {"error": "id not specified"}

    id_with = int(values["id"])

    id = entry.id
    location = entry.location
    x = entry.x
    y = entry.y
    tz = entry.tz

    country = GazCountry(location)
    unit_distance, unit_height = Units(country)

    SetLocale(country)

    dict = {}
    dict["id"] = id_with
    prev, next = PreviousNextResult(id, id_with)
    dict["id_previous"] = prev
    dict["id_next"] = next

    entry = (
        db.session.query(ProfileModel).filter(ProfileModel.id == id_with, ProfileModel.verified.is_(True)).one_or_none()
    )
    if not entry:
        dict["error"] = "This member doesn't exist or has removed their account."
        return dict

    if Blocked(id_with, id):
        dict["error"] = "This member has blocked you."
        return dict

    dict["entry"] = ListMember(db.session, entry, 0, location, x, y, tz, unit_distance)
    dict["name"] = entry.name
    dict["action"] = "member"

    spammer = spam.AnalyseSpammer(id_with)

    image = PhotoFilename(MasterPhoto(db.session, id_with))
    emails = []
    entries = (
        db.session.query(EmailModel)
        .filter(
            or_(
                and_(EmailModel.id_from == id, EmailModel.id_to == id_with),
                and_(EmailModel.id_from == id_with, EmailModel.id_to == id),
            )
        )
        .order_by(EmailModel.sent.desc())
        .all()
    )
    for entry in entries:
        d = {}
        d["sent"] = entry.id_from == id
        d["message"] = entry.message
        d["image"] = entry.image
        d["time"] = Since(entry.sent, False)
        d["viewed"] = entry.viewed
        if d["message"] and not d["sent"]:
            d["spam"] = spam.IsSpamFactored(spam.AnalyseSpam(d["message"]), spammer, 2)
        emails.append(d)
    dict["entries"] = emails

    db.session.query(EmailModel).filter(EmailModel.id_from == id_with, EmailModel.id_to == id).update(
        {"viewed": True}, synchronize_session=False
    )
    db.session.commit()

    return dict


def handle_inbox(entry, values):
    page = int(values.get("page", 0))
    per_page = int(values.get("per_page", PER_PAGE))

    id = entry.id
    location = entry.location
    x = entry.x
    y = entry.y
    tz = entry.tz

    query = db.session.query(
        ProfileModel.id,
        ProfileModel.x,
        ProfileModel.y,
        ProfileModel.name,
        ProfileModel.gender,
        ProfileModel.dob,
        ProfileModel.ethnicity,
        ProfileModel.location,
        ProfileModel.summary,
        ProfileModel.last_login,
        ProfileModel.last_ip_country,
        ProfileModel.created,
        EmailModel.id_from,
    ).join(EmailModel, EmailModel.id_from == ProfileModel.id)

    # Remove any mutually blocked profiles
    blocked_by_me = aliased(BlockedModel)
    blocked_by_them = aliased(BlockedModel)
    query = (
        query.outerjoin(
            blocked_by_me, and_(blocked_by_me.id == EmailModel.id_to, blocked_by_me.id_block == EmailModel.id_from)
        )
        .outerjoin(
            blocked_by_them,
            and_(blocked_by_them.id == EmailModel.id_from, blocked_by_them.id_block == EmailModel.id_to),
        )
        .filter(blocked_by_me.id.is_(None))
        .filter(blocked_by_them.id.is_(None))
    )

    entries = (
        query.filter(EmailModel.id_to == id)
        .group_by(EmailModel.id_from)
        .group_by(ProfileModel.id)
        .order_by(func.max(EmailModel.sent).desc())
        .all()
    )
    ids = [entry.id_from for entry in entries]

    SaveResults(id, ids)

    total = len(entries)
    entries = entries[page * per_page : (page + 1) * per_page]
    ids = [entry.id_from for entry in entries]

    counts = []
    for id_from in ids:
        count = (
            db.session.query(func.count())
            .filter(EmailModel.id_from == id_from, EmailModel.id_to == id, EmailModel.viewed.is_(False))
            .scalar()
        )
        counts.append(count)

    country = GazCountry(location)
    unit_distance, unit_height = Units(country)

    SetLocale(country)

    dict = {}
    dict["action"] = "emailthread"
    dict["type"] = "number"
    dict["entries"] = ListMembers(db.session, entries, counts, location, x, y, tz, unit_distance)
    dict["total"] = total
    dict["page"] = page
    dict["per_page"] = per_page

    return dict


def handle_outbox(entry, values):
    page = int(values.get("page", 0))
    per_page = int(values.get("per_page", PER_PAGE))

    id = entry.id
    location = entry.location
    x = entry.x
    y = entry.y
    tz = entry.tz

    query = db.session.query(
        ProfileModel.id,
        ProfileModel.x,
        ProfileModel.y,
        ProfileModel.name,
        ProfileModel.gender,
        ProfileModel.dob,
        ProfileModel.ethnicity,
        ProfileModel.location,
        ProfileModel.summary,
        ProfileModel.last_login,
        ProfileModel.last_ip_country,
        ProfileModel.created,
        EmailModel.id_to,
    ).join(EmailModel, EmailModel.id_to == ProfileModel.id)

    # Remove any mutually blocked profiles
    blocked_by_me = aliased(BlockedModel)
    blocked_by_them = aliased(BlockedModel)
    query = (
        query.outerjoin(
            blocked_by_me, and_(blocked_by_me.id == EmailModel.id_from, blocked_by_me.id_block == EmailModel.id_to)
        )
        .outerjoin(
            blocked_by_them,
            and_(blocked_by_them.id == EmailModel.id_to, blocked_by_them.id_block == EmailModel.id_from),
        )
        .filter(blocked_by_me.id.is_(None))
        .filter(blocked_by_them.id.is_(None))
    )

    entries = (
        query.filter(EmailModel.id_from == id)
        .group_by(EmailModel.id_to)
        .group_by(ProfileModel.id)
        .order_by(func.max(EmailModel.sent).desc())
        .all()
    )
    ids = [entry.id_to for entry in entries]

    SaveResults(id, ids)

    total = len(entries)
    entries = entries[page * per_page : (page + 1) * per_page]
    ids = [entry.id_to for entry in entries]

    counts = []
    for id_to in ids:
        count = (
            db.session.query(func.count())
            .filter(EmailModel.id_from == id, EmailModel.id_to == id_to, EmailModel.viewed.is_(False))
            .scalar()
        )
        counts.append(count)

    country = GazCountry(location)
    unit_distance, unit_height = Units(country)

    SetLocale(country)

    dict = {}
    dict["action"] = "emailthread"
    dict["type"] = "number"
    dict["entries"] = ListMembers(db.session, entries, counts, location, x, y, tz, unit_distance)
    dict["total"] = total
    dict["page"] = page
    dict["per_page"] = per_page

    return dict


def handle_favorites(entry, values):
    id = entry.id
    location = entry.location
    x = entry.x
    y = entry.y
    tz = entry.tz

    query = db.session.query(
        ProfileModel.id,
        ProfileModel.x,
        ProfileModel.y,
        ProfileModel.name,
        ProfileModel.gender,
        ProfileModel.dob,
        ProfileModel.ethnicity,
        ProfileModel.location,
        ProfileModel.summary,
        ProfileModel.last_login,
        ProfileModel.last_ip_country,
        ProfileModel.created,
        FavoriteModel.id_favorite,
    ).join(FavoriteModel, FavoriteModel.id_favorite == ProfileModel.id)

    # Remove any mutually blocked profiles
    blocked_by_me = aliased(BlockedModel)
    blocked_by_them = aliased(BlockedModel)
    query = (
        query.outerjoin(
            blocked_by_me,
            and_(blocked_by_me.id == FavoriteModel.id, blocked_by_me.id_block == FavoriteModel.id_favorite),
        )
        .outerjoin(
            blocked_by_them,
            and_(blocked_by_them.id == FavoriteModel.id_favorite, blocked_by_them.id_block == FavoriteModel.id),
        )
        .filter(blocked_by_me.id.is_(None))
        .filter(blocked_by_them.id.is_(None))
    )

    entries = query.filter(FavoriteModel.id == id).order_by(ProfileModel.last_login).distinct().all()
    ids = [entry.id_favorite for entry in entries]

    SaveResults(id, ids)

    country = GazCountry(location)
    unit_distance, unit_height = Units(country)

    SetLocale(country)

    dict = {}
    dict["action"] = "member"
    dict["type"] = "full"
    dict["entries"] = ListMembers(db.session, entries, None, location, x, y, tz, unit_distance)

    return dict


def handle_blocked(entry, values):
    id = entry.id
    location = entry.location
    x = entry.x
    y = entry.y
    tz = entry.tz

    query = db.session.query(
        ProfileModel.id,
        ProfileModel.x,
        ProfileModel.y,
        ProfileModel.name,
        ProfileModel.gender,
        ProfileModel.dob,
        ProfileModel.ethnicity,
        ProfileModel.location,
        ProfileModel.summary,
        ProfileModel.last_login,
        ProfileModel.last_ip_country,
        ProfileModel.created,
        BlockedModel.id_block,
    ).join(BlockedModel, BlockedModel.id_block == ProfileModel.id)

    entries = query.filter(BlockedModel.id == id).distinct().all()
    ids = [entry.id_block for entry in entries]

    SaveResults(id, ids)

    country = GazCountry(location)
    unit_distance, unit_height = Units(country)

    SetLocale(country)

    dict = {}
    dict["action"] = "member"
    dict["type"] = "full"
    dict["entries"] = ListMembers(db.session, entries, None, location, x, y, tz, unit_distance)

    return dict


def handle_account(entry, values):
    id = entry.id
    email = entry.email
    password = entry.password
    dob = entry.dob

    dict = {}
    dict["email"] = email
    dict["password"] = password
    dict["dob"] = dob

    return dict


def handle_resetpassword(entry, values):
    if "uuid" not in values:
        return {"error": "uuid not specified"}
    if "email" not in values:
        return {"error": "email not specified"}

    uuid = values["uuid"]
    email = values["email"]

    entry = db.session.query(UUIDModel.profile_id).filter(UUIDModel.uuid == UUID(uuid)).one_or_none()
    if not entry:
        return {"error": "This change password link has expired"}

    dict = {}
    dict["uuid"] = uuid
    dict["email"] = email

    return dict


def handle_cancelled(entry, values):
    id = entry.id

    DeleteMember(db.session, id)

    return {}
