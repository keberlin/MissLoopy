import logging

from database import db_init, MISSLOOPY_DB_URI
from emails import *
from mlutils import *
from model import *
from utils import *

logging.basicConfig(filename="/var/log/missloopy/log", logging.INFO)

session = db_init(MISSLOOPY_DB_URI)

entries = session.query(ProfileModel.last_ip).filter(ProfileModel.verified.is_(True)).all()
ips = set([entry.last_ip for entry in entries])

ids = []
with open("bannedips.txt", "r") as file:
    for line in file.readlines():
        ip = line.strip()
        if ip in ips:
            entries = session.query(ProfileModel.id, ProfileModel.email).filter(ProfileModel.last_ip == ip).all()
            for entry in entries:
                ids.append((entry.id, entry.email, ip))

for id, email, ip in ids:
    DeleteMember(session,id)
    EmailKickedStopForumSpam(email)
    logging.info("Kicked due to banned IP address %s %d %s" % (Quote(ip), id, email))
