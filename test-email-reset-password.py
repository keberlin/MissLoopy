from datetime import datetime, timedelta
import uuid

from database import db_init
from emails import EmailResetPassword
from model import ProfileModel, UUIDModel

session = db_init()

email = "keith.hollis@gmail.com"

# Retrieve the password
entry = session.query(ProfileModel).filter(ProfileModel.email == email).one_or_none()
assert entry

now = datetime.utcnow()

# Create a uuid to use in the verification email
item = UUIDModel(profile_id=entry.id, expiry=now + timedelta(minutes=15))
session.add(item)
session.commit()
assert item.uuid

EmailResetPassword(session, email, item.uuid)
