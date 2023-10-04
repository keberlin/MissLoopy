import os

from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from gazetteer import *
from localization import *
from mlhtml import *
from mlutils import *
from model import *
from tzone import *
from units import *
from utils import *

session = db_init(MISSLOOPY_DB_URI)

BASE_DIR = os.path.dirname(__file__)

entries = session.query(PhotoModel.id,PhotoModel.pid).order_by(PhotoModel.created.desc()).limit(200).all()
photos = [(entry.id, PhotoFilename(entry.pid)) for entry in entries]

d = {'title':'New Photos', 'photos':photos}

print RenderY('new-photos.html', d)
