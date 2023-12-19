from datetime import database
import os

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

now = datetime.utcnow()

country = "United States"
tz = "America/New_York"

SetLocale(country)

unit_distance, unit_height = Units(country)

entries = (
    session.query(ProfileModel)
    .filter(ProfileModel.verified.is_(True), ProfileModel.last_login >= since, ProfileModel.last_login < now)
    .all()
)
for entry in entries:

    id = entry[COL_ID]
    location = entry[COL_LOCATION]

    data = html_defaults()

    # About me
    data["id"] = id
    data["name"] = mask.MaskEverything(entry[COL_NAME])
    data["gender"] = Gender(entry[COL_GENDER])
    data["age"] = Age(entry[COL_DOB])
    data["starsign"] = Starsign(entry[COL_DOB])
    data["ethnicity"] = Ethnicity(entry[COL_ETHNICITY])
    data["location"] = entry[COL_LOCATION]
    data["height"] = Height(entry[COL_HEIGHT], unit_height, 2)
    data["weight"] = Weight(entry[COL_WEIGHT])
    data["education"] = Education(entry[COL_EDUCATION])
    data["status"] = Status(entry[COL_STATUS])
    data["smoking"] = Smoking(entry[COL_SMOKING])
    data["drinking"] = Drinking(entry[COL_DRINKING])
    data["summary"] = mask.MaskEverything(entry[COL_SUMMARY])
    data["occupation"] = mask.MaskEverything(entry[COL_OCCUPATION])
    data["description"] = mask.MaskEverything(entry[COL_DESCRIPTION])
    data["last_login"] = Datetime(entry[COL_LAST_LOGIN], tz).strftime("%x")
    data["login_country"] = entry[COL_LAST_IP_COUNTRY]
    data["created"] = Datetime(entry[COL_CREATED2], tz).strftime("%x")
    # Seeking
    data["gender_choice"] = GenderList(entry[COL_GENDER_CHOICE])
    data["age_range"] = Range(entry[COL_AGE_MIN], entry[COL_AGE_MAX])
    data["looking_for"] = mask.MaskEverything(entry[COL_LOOKING_FOR])

    master = MasterPhoto(session, id)
    data["image"] = ImageData(os.path.join(BASE_DIR, "static", PhotoFilename(master)))
    pids = []
    photos = session.query(PhotoModel.pid).filter(PhotoModel.profile_id == id).all()
    for photo in photos:
        pid = photo.pid
        if pid != master:
            pids.append(pid)
    data["images"] = []
    for pid in pids:
        data["images"].append(ImageData(os.path.join(BASE_DIR, "static", PhotoFilename(pid))))

    with open(os.path.join(BASE_DIR, "static", MEMBERS_DIR, "member%d.html" % id), "w") as f:
        data["advert"] = True

        f.write(RenderY("archive.html", data))

session.query(AdminModel).update({"last_dump_member_search": now})
session.commit()
