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

db.execute("SELECT id_from, message FROM emails WHERE message LIKE 'data:image/%%' ORDER BY sent DESC LIMIT 200")
images = [(entry[0], entry[1]) for entry in db.fetchall()]

d = {'title':'New Images', 'images':images}

print RenderY('new-images.html', d)
