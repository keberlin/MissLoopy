import os

import database
from database import db_init, MISSLOOPY_DB_URI
from gazetteer import *
from localization import *
import mask
from mlhtml import *
from mlutils import *
from model import *
from tzone import *
from units import *
from utils import *

BASE_DIR = os.path.dirname(__file__)

session = db_init(MISSLOOPY_DB_URI)

since = session.query(AdminModel.last_dump_member_search).one()

now = datetime.datetime.utcnow()

country = "United States"
tz = "America/New_York"

SetLocale(country)

unit_distance, unit_height = Units(country)

entries = session.query( ProfileModel).filter(ProfileModel.verified.is_(True),ProfileModel.last_login>=since,ProfileModel.last_login<now").all()
for entry in entries:

    id = entry[COL_ID]
    location = entry[COL_LOCATION]

    dict = html_defaults()

    # About me
    dict["id"] = id
    dict["name"] = mask.MaskEverything(entry[COL_NAME])
    dict["gender"] = Gender(entry[COL_GENDER])
    dict["age"] = Age(entry[COL_DOB])
    dict["starsign"] = Starsign(entry[COL_DOB])
    dict["ethnicity"] = Ethnicity(entry[COL_ETHNICITY])
    dict["location"] = entry[COL_LOCATION]
    dict["height"] = Height(entry[COL_HEIGHT], unit_height, 2)
    dict["weight"] = Weight(entry[COL_WEIGHT])
    dict["education"] = Education(entry[COL_EDUCATION])
    dict["status"] = Status(entry[COL_STATUS])
    dict["smoking"] = Smoking(entry[COL_SMOKING])
    dict["drinking"] = Drinking(entry[COL_DRINKING])
    dict["summary"] = mask.MaskEverything(entry[COL_SUMMARY])
    dict["occupation"] = mask.MaskEverything(entry[COL_OCCUPATION])
    dict["description"] = mask.MaskEverything(entry[COL_DESCRIPTION])
    dict["last_login"] = Datetime(entry[COL_LAST_LOGIN], tz).strftime("%x")
    dict["login_country"] = entry[COL_LAST_IP_COUNTRY]
    dict["created"] = Datetime(entry[COL_CREATED2], tz).strftime("%x")
    # Seeking
    dict["gender_choice"] = GenderList(entry[COL_GENDER_CHOICE])
    dict["age_range"] = Range(entry[COL_AGE_MIN], entry[COL_AGE_MAX])
    dict["looking_for"] = mask.MaskEverything(entry[COL_LOOKING_FOR])

    master = MasterPhoto(id)
    dict["image"] = ImageData(os.path.join(BASE_DIR, "static", PhotoFilename(master)))
    pids = []
    photos = session.query(PhotoModel.pid).filter(PhotoModel.id=id").all()
    for photo in photos:
        pid = photo.pid
        if pid != master:
            pids.append(pid)
    dict["images"] = []
    for pid in pids:
        dict["images"].append(ImageData(os.path.join(BASE_DIR, "static", PhotoFilename(pid))))

    with open(os.path.join(BASE_DIR, "static", MEMBERS_DIR, "member%d.html" % id), "w") as f:
        dict["advert"] = True

        f.write(RenderY("archive.html", dict))

session.query(AdminModel).update({"last_dump_member_search":now})
session.commit()
