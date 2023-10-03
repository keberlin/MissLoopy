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

entries = db.session.query(ProfileModel.email).filter(ProfileModel.verified.is_(True)).all()
emails = set([entry.email.lower() for entry in entries])

with open('listed_email_365.txt', 'rb') as csvfile:
  reader = csv.reader(csvfile, quoting=csv.QUOTE_NONE, skipinitialspace=True)
  for row in reader:
    email = row[0].decode('utf-8', 'ignore').lower()
    if email in emails:
      print 'Scammer email address %s is registered' % (email)
      entry = db.session.query(ProfileModel.id,ProfileModel.name,ProfileModel.location,ProfileModel.last_ip_country).filter(func.lower(ProfileModel.email)==email).one()
      print ' ', entry
