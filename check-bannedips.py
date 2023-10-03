from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import MISSLOOPY_DB_URI, db
from mlutils import *
from model import *
from utils import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

entries = db.session.query(Profiles.last_ip).filter(ProfileModel.verified.is_(True)).all()
ips = set([entry.last_ip for entry in entries])

with open('bannedips.txt','r') as file:
  for line in file.readlines():
    ip = line.strip()
    if ip in ips:
      print 'Banned ip address %s is registered' % (ip)
      entries = db.session.query(ProfileModel.id,ProfileModel.name,ProfileModel.last_ip_country).filter(ProfileModel.last_ip==ip).all()
      for entry in entries:
        print ' ', entry
