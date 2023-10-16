from database import db_init, MISSLOOPY_DB_URI
from emails import *
from localization import *
from mlutils import *
from model import *

session = db_init(MISSLOOPY_DB_URI)

entry1 = session.query(ProfileModel).filter(ProfileModel.email == "keith.hollis@gmail.com").one()
entry2 = session.query(ProfileModel).filter(ProfileModel.email == "razeberlin@gmail.com").one()

EmailNotify(entry1, entry2)
