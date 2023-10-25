from datetime import datetime, timedelta

from database import db_init, MISSLOOPY_DB_URI
from emails import *
from logger import logger
from model import *

session = db_init(MISSLOOPY_DB_URI)

now = datetime.utcnow()

entries = session.query(ProfileModel.id, ProfileModel.email).filter(ProfileModel.verified.is_(False)).all()
for entry in entries:
    print(entry.email, entry.id)

    # Create a uuid to use in the verification email
    uuid = UUIDModel(profile_id=entry.id, expiry=now + timedelta(minutes=15))
    db.session.add(entry)
    db.session.commit()
    assert uuid.uuid

    EmailVerify(session, entry.email, uuid.uuid)
