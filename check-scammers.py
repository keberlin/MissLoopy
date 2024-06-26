import csv

from database import db_init
from mlutils import *
from model import *
from utils import *

session = db_init()

entries = session.query(ProfileModel.email).filter(ProfileModel.verified.is_(True)).all()
emails = set([entry.email.lower() for entry in entries])

with open("listed_email_365.txt", "rb") as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONE, skipinitialspace=True)
    for row in reader:
        email = row[0].lower()
        if email in emails:
            print("Scammer email address %s is registered" % (email))
            entry = (
                session.query(ProfileModel.id, ProfileModel.name, ProfileModel.location, ProfileModel.last_ip_country)
                .filter(func.lower(ProfileModel.email) == email)
                .one()
            )
            print(" ", entry)
