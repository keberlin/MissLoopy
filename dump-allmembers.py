#!/usr/bin/python

import os

import database

from utils import *
from gazetteer import *
from mlutils import *
from mlhtml import *

BASE_DIR = os.path.dirname(__file__)

db = database.Database(MISS_LOOPY_DB)

dict = {}

with open(os.path.join(BASE_DIR, 'static', MEMBERS_DIR, 'all.html'), 'w') as f:
  coords = []
  db.execute('SELECT DISTINCT x,y FROM profiles WHERE verified')
  for entry in db.fetchall():
    lat = entry[1]*360.0/CIRCUM_Y
    lng = entry[0]*360.0/CIRCUM_X
    coords.append(lat)
    coords.append(lng)
  dict['coords'] = coords

  f.write(RenderY('all.html', dict))
