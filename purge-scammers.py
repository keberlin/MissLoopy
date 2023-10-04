import csv
import logging

from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from emails import *
from mlutils import *
from model import *
from utils import *

db = db_init(MISSLOOPY_DB_URI)

entries = db.session.query(ProfileModel.email).filter(ProfileModel.verified.is_(True)).all()
emails = set([entry.email.lower() for entry in entries])

ids = []
with open('listed_email_365.txt', 'rb') as csvfile:
  reader = csv.reader(csvfile, quoting=csv.QUOTE_NONE, skipinitialspace=True)
  for row in reader:
    email = row[0].decode('utf-8', 'ignore').lower()
    if email in emails:
      entry = db.session.query(ProfileModel.id).filter(func.lower(ProfileModel.email)==email).one()
      ids.append((entry.id, email))

for id, email in ids:
  DeleteMember(id)
  EmailKickedStopForumSpam(email)
  logging.info('Kicked due to banned email address %d %s' % (id, email))
