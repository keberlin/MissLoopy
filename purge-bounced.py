import csv

from database import db_init, MISSLOOPY_DB_URI
from logger import logger
from mlutils import *
from model import *
from utils import *

session = db_init(MISSLOOPY_DB_URI)

bounced = set()
with open("bounced.log", "r") as f:
    for email in f.readlines():
        bounced.add(email)

entries = session.query(ProfileModel.email).filter(ProfileModel.verified.is_(True)).all()
emails = set([entry.email.lower() for entry in entries])

for email in emails.intersection(bounced):
    entry = session.query(ProfileModel.id).filter(func.lower(ProfileModel.email) == email).one()
    id = entry.id
    DeleteMember(session, id)
