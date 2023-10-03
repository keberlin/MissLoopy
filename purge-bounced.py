import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import MISSLOOPY_DB_URI, db
from mlutils import *
from model import *
from utils import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

bounced = set()
with open('bounced.log', 'r') as f:
  for email in f.readlines():
    bounced.add(email)

entries = db.session.query(ProfileModel.email).filter(ProfileModel.verified.is_(True)).all()
emails = set([entry.email.lower() for entry in entries])

for email in emails.intersection(bounced):
  entry = db.session.query(ProfileModel.id).filter(func.lower(ProfileModel.email)==email).one()
  id = entry.id
  DeleteMember(id)
