import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import *
from gazetteer import *
from mlutils import *
from database import MISSLOOPY_DB_URI, db
from model import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

ids = set()
with open('junk-auto.log', 'r') as file:
  for line in file.readlines():
    line = line.decode('utf-8','ignore')
    words = line.split()
    ids.add(int(words[0]))
with open('junk-reported.log', 'r') as file:
  for line in file.readlines():
    line = line.decode('utf-8','ignore')
    words = line.split()
    try:
      ids.add(int(words[0]))
    except:
      pass

ids = list(ids)
ids.sort()
ids.reverse()
for id in ids:
  entry = db.session.query(ProfilesModel).filter(ProfilesModel.id==id).one_or_none()
  if not entry:
    continue
  ip = entry.last_ip
  email = entry.email
  name = entry.name
  country = GazCountry(entry.location)
  last_login_country = entry.last_ip_country
  entry = db.session.query(EmailsModel.message).filter(EmailsModel.id_from==id).order_by(func.length(EmailsModel.message).desc()).first()
  if not entry:
    continue
  message = entry.message
  members = db.session.query(func.count(EmailsModel.id_to.distinct())).filter(EmailsModel.id_from==id).scalar()
  out = '%d: %d, %s, %s, "%s", %s, (%s), "%s"' % (id, members, ip, email, name, country, last_login_country, message)
  print out.encode('utf-8')
