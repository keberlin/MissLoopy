from datetime import datetime, timedelta

from database import db_init
from model import *

session = db_init()

now = datetime.utcnow()

# Delete any expired uuids
session.query(UUIDModel).filter(UUIDModel.expiry <= now).delete()
session.commit()

# Delete any unverified profiles after 1 month
td = now - timedelta(days=30)
session.query(ProfileModel).filter(ProfileModel.verified.is_(False), ProfileModel.created < td).delete()
session.commit()

# Delete all emails older than 6 months
td = now - timedelta(days=30 * 6)
session.query(EmailModel).filter(EmailModel.sent < td).delete()
session.commit()
