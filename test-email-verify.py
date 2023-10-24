from datetime import datetime, timedelta

from database import db_init, MISSLOOPY_DB_URI
from emails import EmailVerify
from model import ProfileModel, UUIDModel

session = db_init(MISSLOOPY_DB_URI)

email = "keith.hollis@gmail.com"

# Retrieve the password
entry = session.query(ProfileModel).filter(ProfileModel.email == email).one_or_none()
assert entry

now = datetime.utcnow()

item = UUIDModel(profile_id=entry.id, expiry=now + timedelta(minutes=15))
session.add(item)
session.commit()
assert item.uuid

EmailVerify(session, email, item.uuid)
