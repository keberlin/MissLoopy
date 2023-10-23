import csv
import logging

from database import db_init, MISSLOOPY_DB_URI
from emails import *
from mlutils import *
from model import *
from utils import *

logging.basicConfig(filename="/var/log/missloopy/log", logging.INFO)

session = db_init(MISSLOOPY_DB_URI)

entries = session.query(ProfileModel.email).filter(ProfileModel.verified.is_(True)).all()
emails = set([entry.email.lower() for entry in entries])

ids = []
with open("listed_email_365.txt", "r") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONE, skipinitialspace=True)
    for row in reader:
        email = row[0].lower()
        if email in emails:
            entry = session.query(ProfileModel.id).filter(func.lower(ProfileModel.email) == email).one()
            ids.append((entry.id, email))

for id, email in ids:
    DeleteMember(session,id)
    EmailKickedStopForumSpam(email)
    logging.info("Kicked due to banned email address %d %s" % (id, email))
