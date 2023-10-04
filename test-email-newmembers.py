from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from emails import *
from localization import *
from mlutils import *
from model import *

db = db_init(MISSLOOPY_DB_URI)

entry = db.session.query(ProfileModel).filter(ProfileModel.email=='keith.hollis@gmail.com').one()

members = [15, 18, 25, 27, 35]

EmailNewMembers(entry, members)
