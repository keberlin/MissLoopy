import hashlib
import re

from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from mlutils import *
from model import *
from utils import *

session = db_init(MISSLOOPY_DB_URI)

entries = session.query(ProfileModel).limit(10).all() # TODO Remove the limit
for entry in entries:
  print(entry.password, hashlib.md5(entry.password.encode()).hexdigest())
  #session.query(ProfileModel).filter(ProfileModel.id==id).update({"password":hashlib.md5(entry.password.encode()).hexdigest()},synchronize_session=False)
session.commit()
