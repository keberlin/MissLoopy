import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import *
from mlutils import *
from emails import *
from database import MISSLOOPY_DB_URI, db
from model import *

from logger import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

parser = argparse.ArgumentParser(description='Delete Members.')
parser.add_argument('id', nargs='+', help='member ids to be deleted')
args = parser.parse_args()

for id in args.id:
  id = int(id)
  entry = db.session.query(ProfilesModel).filter(ProfilesModel.id==id).one_or_none()
  if not entry:
    continue
  ip = entry.last_ip
  email = entry.email
  name = entry.name
  entry = db.session.query(EmailsModel.message).filter(EmailsModel.id_from==id).order_by(EmailsModel.sent.desc()).first()
  if not entry:
    continue
  message = entry.message
  StopForumSpamAdd(name,email,ip,message)
  DeleteMember(id)
  EmailKicked(email)
  logger.info('Kicked %d %s' % (id, email))
