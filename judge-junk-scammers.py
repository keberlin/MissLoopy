import csv

from database import db_init
from emails import *
from gazetteer import *
from logger import logger
from mlutils import *
from model import EmailModel, ProfileModel
from urlutils import StopForumSpamAdd

session = db_init()

ids = set()
with open("junk-auto.log", "r") as file:
    for line in file.readlines():
        line = line
        words = line.split()
        ids.add(words[0])
with open("junk-reported.log", "r") as file:
    for line in file.readlines():
        line = line
        words = line.split()
        ids.add(words[0])

for id in ids:
    entry = session.query(ProfileModel).filter(ProfileModel.id == id).one_or_none()
    if not entry:
        continue
    ip = entry.last_ip
    email = entry.email
    name = entry.name
    country = GazCountry(entry.location)
    last_login_country = entry.last_ip_country
    entry = (
        session.query(EmailModel.message)
        .filter(EmailModel.id_from == id)
        .filter(EmailModel.message.is_not(None))
        .order_by(func.length(EmailModel.message).desc())
        .first()
    )
    if not entry:
        continue
    message = entry.message
    members = session.query(func.count(EmailModel.id_to.distinct())).filter(EmailModel.id_from == id).scalar()
    out = '%d: %d, %s, %s, "%s", %s, (%s), "%s"' % (id, members, ip, email, name, country, last_login_country, message)
    entries = session.query(EmailModel.id_to.distinct()).filter(EmailModel.id_from == id).all()
    id_tos = [entry[0] for entry in entries]
    tos = []
    for id_to in id_tos[:10]:
        entry = session.query(ProfileModel).filter(ProfileModel.id == id_to).one()
        to = '%d: "%s", %s' % (id_to, entry.name, GazCountry(entry.location))
        tos.append(to)
    print
    print
    print(out)
    for to in tos:
        print("  ", to)
    print
    kick = raw_input("Kick? ")
    if kick == "y":
        StopForumSpamAdd(name, email, ip, message)
        DeleteMember(session, id)
        EmailKicked(session, email)
        logger.info(f"Kicked due to spamming {ip} {id} {email}")
    elif kick == "q":
        break
