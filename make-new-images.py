import os

from database import db_init
from gazetteer import *
from localization import *
from logger import logger
from mlhtml import *
from mlutils import *
from model import *
from tzone import *
from units import *
from utils import *

session = db_init()

BASE_DIR = os.path.dirname(__file__)

entries = (
    session.query(EmailModel.id_from, EmailModel.image)
    .filter(EmailModel.image.is_not(None))
    .order_by(EmailModel.sent.desc())
    .limit(200)
    .all()
)
images = [(entry.id_from, entry.image) for entry in entries]

d = {"title": "New Images", "images": images}

print(RenderY("new-images.html", d))
