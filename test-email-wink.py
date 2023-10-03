from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import MISSLOOPY_DB_URI, db
from emails import *
from localization import *
from mlutils import *
from model import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

entry1 = db.session.query(ProfileModel).filter(ProfileModel.email=='keith.hollis@gmail.com').one()
entry2 = db.session.query(ProfileModel).filter(ProfileModel.email=='razeberlin@gmail.com').one()

EmailWink(entry1, entry2)
