import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database
from database import MISSLOOPY_DB_URI, db
from mlutils import *
from model import *
from utils import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

email = sys.argv[1]

entry = db.session.query(ProfileModel.id).filter(func.lower(ProfileModel.email)==email).one_or_none()
if entry:
  id = entry.id
  print id
