# from localization import *
# from mlutils import *
from database import db_init, MISSLOOPY_DB_URI
from emails import EmailNewMembers
from model import ProfileModel

session = db_init(MISSLOOPY_DB_URI)

email = "keith.hollis@gmail.com"

entry = session.query(ProfileModel).filter(ProfileModel.email == email).one()

members = session.query(ProfileModel).filter(ProfileModel.id.in_([15, 18, 25, 27, 35])).all()

EmailNewMembers(session, entry, members)
