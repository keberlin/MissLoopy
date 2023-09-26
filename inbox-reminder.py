import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mlutils import *
from emails import *
from database import MISSLOOPY_DB_URI, db
from model import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

now = datetime.datetime.utcnow()
since = now-datetime.timedelta(days=14)

entries = db.session.query(ProfilesModel.id).join(EmailsModel,EmailsModel.id_to==ProfilesModel.id).filter(EmailsModel.viewed.is_(False),EmailsModel.sent<since).distinct().all()
ids = (entry.id for entry in entries)

for id in ids:
  entry = db.session.query(ProfilesModel.email,ProfilesModel.name).filter(ProfilesModel.id==id).one()
  email = entry.email
  name  = entry.name
  EmailInboxReminder(email, name)
