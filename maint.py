import re, hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import *
from mlutils import *
from database import MISSLOOPY_DB_URI, db
from model import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

entries = db.session.query(ProfilesModel).limit(10).all() # TODO Remove the limit
for entry in entries:
  print(entry.password, hashlib.md5(entry.password.encode()).hexdigest())
  #db.session.query(ProfilesModel).filter(ProfilesModel.id==id).update({"password":hashlib.md5(entry.password.encode()).hexdigest()},synchronize_session=False)
db.session.commit()
