#!/usr/bin/python

import os

import database, mask

from utils import *
from units import *
from tzone import *
from localization import *
from gazetteer import *
from mlutils import *
from mlhtml import *

BASE_DIR = os.path.dirname(__file__)

db = database.Database(MISS_LOOPY_DB)

db.execute("SELECT id, pid FROM photos ORDER BY pid DESC LIMIT 200")
for entry in db.fetchall():
  print entry[0], PhotoFilename(entry[1])
