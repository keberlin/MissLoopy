import csv

from database import db_init
from mlutils import *
from model import *
from utils import *

session = db_init()

bounced = set()
with open("bounced.log", "r") as f:
    for email in f.readlines():
        bounced.add(email)

entries = session.query(ProfileModel.email).filter(ProfileModel.verified.is_(True)).all()
emails = set([entry.email.lower() for entry in entries])

for email in emails.intersection(bounced):
    print("Bounced email address %s is registered" % (email))
    entry = (
        session.query(ProfileModel.id, ProfileModel.name, ProfileModel.location, ProfileModel.last_ip)
        .filter(func.lower(ProfileModel.email) == email)
        .one()
    )
    print(" ", entry)
