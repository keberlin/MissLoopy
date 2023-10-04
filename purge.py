import datetime

from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from model import *

db = db_init(MISSLOOPY_DB_URI)

now = datetime.datetime.utcnow()

# Delete any unverified profiles after 1 month
td = now-datetime.timedelta(days=30)
db.session.query(ProfileModel).filter(ProfileModel.verified.is_(False),ProfileModel.created2<td).delete()
db.session.commit()

# Delete all emails older than 6 months
td = now-datetime.timedelta(days=30*6)
db.session.query(EmailModel).filter(EmailModel.sent<td).delete()
db.session.commit()
