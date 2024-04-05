import csv

from database import db_init
from gazetteer import *
from mlutils import *
from model import *
from utils import *

session = db_init()

ids = set()
with open("junk-auto.log", "r") as file:
    for line in file.readlines():
        line = line
        words = line.split()
        ids.add(int(words[0]))
with open("junk-reported.log", "r") as file:
    for line in file.readlines():
        line = line
        words = line.split()
        try:
            ids.add(int(words[0]))
        except:
            pass

ids = list(ids)
ids.sort()
ids.reverse()
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
        .order_by(func.length(EmailModel.message).desc())
        .first()
    )
    if not entry:
        continue
    message = entry.message
    members = session.query(func.count(EmailModel.id_to.distinct())).filter(EmailModel.id_from == id).scalar()
    out = '%d: %d, %s, %s, "%s", %s, (%s), "%s"' % (id, members, ip, email, name, country, last_login_country, message)
    print(out)
