import os

from database import db_init, MISSLOOPY_DB_URI
from gazetteer import *
from localization import *
from mlhtml import *
from mlutils import *
from model import *
from tzone import *
from units import *
from utils import *

BASE_DIR = os.path.dirname(__file__)

logging.basicConfig(filename="/var/log/missloopy/log", logging.INFO)

session = db_init(MISSLOOPY_DB_URI)

entries = session.query(PhotoModel.profile_id, PhotoModel.pid).order_by(PhotoModel.created.desc()).limit(200).all()
photos = [(entry.profile_id, PhotoFilename(entry.pid)) for entry in entries]

d = {"title": "New Photos", "photos": photos}

print(RenderY("new-photos.html", d))
