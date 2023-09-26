from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mlutils import *
from emails import *
from database import MISSLOOPY_DB_URI, db
from model import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

entries = db.session.query(ProfilesModel.id,ProfilesModel.email).filter(ProfilesModel.verified.is_(False)).all()
for entry in entries:
  print entry.email.encode('utf-8'), entry.id
  EmailVerify(entry.email, entry.id)
