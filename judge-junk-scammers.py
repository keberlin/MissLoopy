import csv, requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import *
from gazetteer import *
from mlutils import *
from emails import *
from database import MISSLOOPY_DB_URI, db
from model import *

from logger import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

ids = set()
with open('junk-auto.log', 'r') as file:
  for line in file.readlines():
    line = line.decode('utf-8','ignore')
    words = line.split()
    ids.add(words[0])
with open('junk-reported.log', 'r') as file:
  for line in file.readlines():
    line = line.decode('utf-8','ignore')
    words = line.split()
    ids.add(words[0])

entries = db.session.query(EmailsModel.id_from,func.max(EmailsModel.sent)).filter(EmailsModel.id_from.in_(ids)).group_by(EmailsModel.id_from).order_by(func.max(EmailsModel.sent).desc()).all()
ids = [x.id_from for x in entries]

for id in ids:
  entry = db.session.query(ProfilesModel).filter(ProfilesModel.id==id).one_or_none()
  if not entry:
    continue
  ip = entry.last_ip
  email = entry.email
  name = entry.name
  country = GazCountry(entry.location)
  last_login_country = entry.last_ip_country
  entry = db.session.query(EmailsModel.message).filter(EmailsModel.id_from==id).filter(EmailsModel.message.is_not(None)).order_by(func.length(EmailsModel.message).desc()).first()
  #db.execute("SELECT message, sent FROM emails WHERE id_from=%d AND NOT message IS NULL ORDER BY LENGTH(message) DESC LIMIT 1" % (id))
  if not entry:
    continue
  message = entry.message
  members = db.session.query(func.count(EmailsModel.id_to.distinct())).filter(EmailsModel.id_from==id).scalar()
  out = '%d: %d, %s, %s, "%s", %s, (%s), "%s"' % (id, members, ip, email, name, country, last_login_country, message)
  entries = db.session.query(EmailsModel.id_to.distinct()).filter(EmailsModel.id_from==id).all()
  id_tos = [entry[0] for entry in entries]
  tos = []
  for id_to in id_tos[:10]:
    entry = db.session.query(ProfilesModel).filter(ProfilesModel.id==id_to).one()
    to = '%d: "%s", %s' % (id_to, entry.name, GazCountry(entry.location))
    tos.append(to)
  print
  print
  print out.encode('utf-8')
  for to in tos:
    print '  ', to.encode('utf-8')
  print
  kick = raw_input('Kick? ')
  if kick=='y':
    StopForumSpamAdd(name,email,ip,message)
    DeleteMember(id)
    EmailKicked(email)
    logger.info('Kicked due to spamming %s %d %s' % (Quote(ip), id, email))
  elif kick=='q':
    break
