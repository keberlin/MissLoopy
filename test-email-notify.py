from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from emails import *
from localization import *
from mlutils import *
from model import *

db = db_init(MISSLOOPY_DB_URI)

entry1 = db.session.query(ProfileModel).filter(ProfileModel.email=='keith.hollis@gmail.com').one()
entry2 = db.session.query(ProfileModel).filter(ProfileModel.email=='razeberlin@gmail.com').one()

EmailNotify(entry1, entry2)
