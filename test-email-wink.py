from database import db_init, MISSLOOPY_DB_URI
from emails import *
from localization import *
from mlutils import *
from model import *

session = db_init(MISSLOOPY_DB_URI)

email1 = "keith.hollis@gmail.com"
email2 = "razeberlin@gmail.com"

entry1 = session.query(ProfileModel).filter(ProfileModel.email == email1).one()
entry2 = session.query(ProfileModel).filter(ProfileModel.email == email2).one()

EmailWink(session, entry1, entry2)
