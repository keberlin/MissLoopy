import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import MISSLOOPY_DB_URI, db
from emails import *
from mlutils import *
from model import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

parser = argparse.ArgumentParser(description='Delete Photos.')
parser.add_argument('pid', nargs='+', help='photo ids to be deleted')
args = parser.parse_args()

for pid in args.pid:
  pid = int(pid)
  entry = db.session.query(EmailModel.id).filter(PhotoModel.pid==pid).one()
  id = entry.id
  entry = db.session.query(ProfileModel.email).filter(ProfileModel.id==id).one()
  email = entry.email
  DeletePhoto(pid)
  EmailPhotoDeleted(email)
