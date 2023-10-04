import os

from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from gazetteer import *
from mlhtml import *
from mlutils import *
from model import *
from utils import *

db = db_init(MISSLOOPY_DB_URI)

BASE_DIR = os.path.dirname(__file__)

dict = {}

with open(os.path.join(BASE_DIR, 'static', MEMBERS_DIR, 'all.html'), 'w') as f:
  coords = []
  entries = db.session.query(ProfileModel.x,ProfileModel.y).filter(ProfileModel.verified.is_(True)).distinct().all()
  for entry in entries:
    lat = entry[1]*360.0/CIRCUM_Y
    lng = entry[0]*360.0/CIRCUM_X
    coords.append(lat)
    coords.append(lng)
  dict['coords'] = coords

  f.write(RenderY('all.html', dict))
