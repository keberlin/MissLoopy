import hashlib
import re

from database import db_init, MISSLOOPY_DB_URI
from mlutils import *
from model import *
from utils import *

session = db_init(MISSLOOPY_DB_URI)

entries = session.query(ProfileModel).limit(10).all()  # TODO Remove the limit
for entry in entries:
    print(entry.password, hashlib.md5(entry.password.encode()).hexdigest())
    # session.query(ProfileModel).filter(ProfileModel.id==id).update({"password":hashlib.md5(entry.password.encode()).hexdigest()},synchronize_session=False)
session.commit()
