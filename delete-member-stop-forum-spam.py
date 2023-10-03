import argparse
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

parser = argparse.ArgumentParser(description='Delete Members.')
parser.add_argument('id', nargs='+', help='member ids to be deleted')
args = parser.parse_args()

for id in args.id:
  id = int(id)
  entry = db.session.query(ProfileModel).filter(ProfileModel.id==id).one_or_none()
  if not entry:
    continue
  ip = entry.last_ip
  email = entry.email
  name = entry.name
  entry = db.session.query(EmailModel.message).filter(EmailModel.id_from==id).order_by(EmailModel.sent.desc()).first()
  if not entry:
    continue
  message = entry.message
  StopForumSpamAdd(name,email,ip,message)
  DeleteMember(id)
  EmailKicked(email)
  logging.info('Kicked %d %s' % (id, email))
