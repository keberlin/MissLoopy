import argparse
import logging

from database import db_init, MISSLOOPY_DB_URI
from emails import *
from mlutils import *
from model import *
from utils import *

logging.basicConfig(filename="/var/log/missloopy/log", logging.INFO)

session = db_init(MISSLOOPY_DB_URI)

parser = argparse.ArgumentParser(description="Delete Members.")
parser.add_argument("id", nargs="+", help="member ids to be deleted")
args = parser.parse_args()

for id in args.id:
    id = int(id)
    entry = session.query(ProfileModel).filter(ProfileModel.id == id).one_or_none()
    if not entry:
        continue
    ip = entry.last_ip
    email = entry.email
    name = entry.name
    entry = session.query(EmailModel.message).filter(EmailModel.id_from == id).order_by(EmailModel.sent.desc()).first()
    if not entry:
        continue
    message = entry.message
    StopForumSpamAdd(name, email, ip, message)
    DeleteMember(session,id)
    EmailKicked(email)
    logging.info("Kicked %d %s" % (id, email))
