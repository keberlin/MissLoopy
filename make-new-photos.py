#!/usr/bin/python

import os

import database

from utils import *
from units import *
from tzone import *
from localization import *
from gazetteer import *
from mlutils import *
from mlhtml import *

BASE_DIR = os.path.dirname(__file__)

db = database.Database(MISS_LOOPY_DB)

db.execute("SELECT id, pid FROM photos ORDER BY created DESC LIMIT 200")
photos = [(entry[0], PhotoFilename(entry[1])) for entry in db.fetchall()]

d = {'title':'New Photos', 'photos':photos}

print RenderY('new-photos.html', d)
