from database import db_init, MISSLOOPY_DB_URI
from emails import *
from model import *

logging.basicConfig(filename="/var/log/missloopy/log", level=logging.INFO)

session = db_init(MISSLOOPY_DB_URI)

now = datetime.datetime.utcnow()

entries = session.query(ProfileModel.id, ProfileModel.email).filter(ProfileModel.verified.is_(False)).all()
for entry in entries:
    print(entry.email, entry.id)

    # Create a uuid to use in the verification email
    uuid = UUIDModel(profile_id=entry.id, created=now)
    db.session.add(entry)
    db.session.commit()
    assert uuid.uuid

    EmailVerify(entry.email, uuid)
