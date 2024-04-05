import os

from database import db_init
from gazetteer import *
from mlhtml import *
from mlutils import *
from model import ProfileModel
from utils import *

session = db_init()

BASE_DIR = os.path.dirname(__file__)

data = {}

with open(os.path.join(BASE_DIR, "static", MEMBERS_DIR, "all.html"), "w") as f:
    coords = []
    entries = session.query(ProfileModel.x, ProfileModel.y).filter(ProfileModel.verified.is_(True)).distinct().all()
    for entry in entries:
        lat = entry[1] * 360.0 / CIRCUM_Y
        lng = entry[0] * 360.0 / CIRCUM_X
        coords.append(lat)
        coords.append(lng)
    data["coords"] = coords

    f.write(RenderY("all.html", data))
