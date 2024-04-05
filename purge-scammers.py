import csv

from sqlalchemy.sql import func

from database import db_init
from emails import EmailKickedStopForumSpam
from logger import logger
from mlutils import DeleteMember
from model import ProfileModel

# from utils import *


session = db_init()

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
    DeleteMember(session, id)
    EmailKickedStopForumSpam(session, email)
    logger.info("Kicked due to banned email address %d %s" % (id, email))
