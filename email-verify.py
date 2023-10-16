from database import db_init, MISSLOOPY_DB_URI
from emails import *
from mlutils import *
from model import *

session = db_init(MISSLOOPY_DB_URI)

entries = session.query(ProfileModel.id, ProfileModel.email).filter(ProfileModel.verified.is_(False)).all()
for entry in entries:
    print(entry.email, entry.id)
    EmailVerify(entry.email, entry.id)
