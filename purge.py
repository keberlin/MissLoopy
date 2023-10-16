import datetime

from database import db_init, MISSLOOPY_DB_URI
from model import *

session = db_init(MISSLOOPY_DB_URI)

now = datetime.datetime.utcnow()

# Delete any unverified profiles after 1 month
td = now - datetime.timedelta(days=30)
session.query(ProfileModel).filter(ProfileModel.verified.is_(False), ProfileModel.created2 < td).delete()
session.commit()

# Delete all emails older than 6 months
td = now - datetime.timedelta(days=30 * 6)
session.query(EmailModel).filter(EmailModel.sent < td).delete()
session.commit()
