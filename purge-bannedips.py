import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import MISSLOOPY_DB_URI, db
from emails import *
from mlutils import *
from model import *
from utils import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

entries = db.session.query(ProfileModel.last_ip).filter(ProfileModel.verified.is_(True)).all()
ips = set([entry.last_ip for entry in entries])

ids = []
with open('bannedips.txt','r') as file:
  for line in file.readlines():
    ip = line.strip()
    if ip in ips:
      entries = db.session.query(ProfileModel.id,ProfileModel.email).filter(ProfileModel.last_ip==ip).all()
      for entry in entries:
        ids.append((entry.id, entry.email, ip))

for id, email, ip in ids:
  DeleteMember(id)
  EmailKickedStopForumSpam(email)
  logging.info('Kicked due to banned IP address %s %d %s' % (Quote(ip), id, email))
