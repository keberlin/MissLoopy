import os

from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from emails import *
from mlutils import *
from model import *

db = db_init(MISSLOOPY_DB_URI)

now = datetime.datetime.utcnow()
since = now-datetime.timedelta(days=14)

entries = db.session.query(ProfileModel.id).join(EmailModel,EmailModel.id_to==ProfileModel.id).filter(EmailModel.viewed.is_(False),EmailModel.sent<since).distinct().all()
ids = (entry.id for entry in entries)

for id in ids:
  entry = db.session.query(ProfileModel.email,ProfileModel.name).filter(ProfileModel.id==id).one()
  email = entry.email
  name  = entry.name
  EmailInboxReminder(email, name)
