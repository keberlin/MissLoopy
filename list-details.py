import sys

import database
from database import db_init, MISSLOOPY_DB_URI
from mlutils import *
from model import *
from utils import *

session = db_init(MISSLOOPY_DB_URI)

id = int(sys.argv[1])

entry = (
    session.query(ProfileModel.last_ip, ProfileModel.email, ProfileModel.name)
    .filter(ProfileModel.id == id)
    .one_or_none()
)
if entry:
    ip = entry.last_ip
    email = entry.email
    name = entry.name
    messages = []
    entries = session.query(EmailModel.message).filter(EmailModel.id_from == id).all()
    for entry in entries:
        messages.append(entry.message)
    members = session.query(func.count(EmailModel.id_to.distinct())).filter(EmailModel.id_from == id).scalar()
    str = '%d: %d, %s, %s, "%s", "%s"' % (id, members, ip, email, name, str(messages))
    print(str)
