import csv
import logging

import requests

from database import db_init, MISSLOOPY_DB_URI
from emails import *
from gazetteer import *
from mlutils import *
from model import *
from utils import *

logging.basicConfig(filename="/var/log/missloopy/log", level=logging.INFO)

session = db_init(MISSLOOPY_DB_URI)

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

entries = (
    session.query(EmailModel.id_from, func.max(EmailModel.sent))
    .filter(EmailModel.id_from.in_(ids))
    .group_by(EmailModel.id_from)
    .order_by(func.max(EmailModel.sent).desc())
    .all()
)
ids = [x.id_from for x in entries]

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
        logging.info("Kicked due to spamming %s %d %s" % (Quote(ip), id, email))
    elif kick == "q":
        break
