import sys

import database
from database import db_init
from mlutils import *
from model import *
from utils import *

session = db_init()

email = sys.argv[1]

entry = session.query(ProfileModel.id).filter(func.lower(ProfileModel.email) == email).one_or_none()
if entry:
    id = entry.id
    print(id)
