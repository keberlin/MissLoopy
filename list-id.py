import sys

from sqlalchemy import create_engine

import database
from database import MISSLOOPY_DB_URI, db_init
from mlutils import *
from model import *
from utils import *

session = db_init(MISSLOOPY_DB_URI)

email = sys.argv[1]

entry = session.query(ProfileModel.id).filter(func.lower(ProfileModel.email)==email).one_or_none()
if entry:
  id = entry.id
  print id
