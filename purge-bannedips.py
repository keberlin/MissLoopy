from database import db_init
from emails import EmailKickedStopForumSpam
from logger import logger
from mlutils import DeleteMember
from model import ProfileModel

# from utils import *

session = db_init()

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
    DeleteMember(session, id)
    EmailKickedStopForumSpam(session, email)
    logger.info(f"Kicked due to banned IP address {ip} {id} {email}")
