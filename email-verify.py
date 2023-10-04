from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from emails import *
from mlutils import *
from model import *

db = db_init(MISSLOOPY_DB_URI)

entries = db.session.query(ProfileModel.id,ProfileModel.email).filter(ProfileModel.verified.is_(False)).all()
for entry in entries:
  print entry.email.encode('utf-8'), entry.id
  EmailVerify(entry.email, entry.id)
