from datetime import datetime, timedelta
import os

from database import db_init, MISSLOOPY_DB_URI
from emails import *
from mlutils import *
from model import *

logging.basicConfig(filename="/var/log/missloopy/log", level=logging.INFO)

session = db_init(MISSLOOPY_DB_URI)

now = datetime.utcnow()
since = now - timedelta(days=14)

entries = (
    session.query(ProfileModel.id)
    .join(EmailModel, EmailModel.id_to == ProfileModel.id)
    .filter(EmailModel.viewed.is_(False), EmailModel.sent < since)
    .distinct()
    .all()
)
ids = (entry.id for entry in entries)

for id in ids:
    entry = session.query(ProfileModel.email, ProfileModel.name).filter(ProfileModel.id == id).one()
    email = entry.email
    name = entry.name
    EmailInboxReminder(email, name)
