import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import MISSLOOPY_DB_URI, db
from gazetteer import *
from localization import *
from mlhtml import *
from mlutils import *
from model import *
from tzone import *
from units import *
from utils import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

BASE_DIR = os.path.dirname(__file__)

entries = db.session.query(PhotoModel.id,PhotoModel.pid).order_by(PhotoModel.created.desc()).limit(200).all()
photos = [(entry.id, PhotoFilename(entry.pid)) for entry in entries]

d = {'title':'New Photos', 'photos':photos}

print RenderY('new-photos.html', d)
