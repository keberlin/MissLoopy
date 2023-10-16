import csv
import sys

from database import db_init, MISSLOOPY_DB_URI
from mlutils import *
from model import *
from utils import *

session = db_init(MISSLOOPY_DB_URI)

print("Dumping profiles..")
with open("profiles.csv", "w") as output:
    writer = csv.writer(output)
    entries = session.query(ProfileModel).all()
    for entry in entries:
        fields = map(lambda x: x if isinstance(x, unicode) else x, entry)
        writer.writerow(fields)

print("Dumping photos..")
with open("photos.csv", "w") as output:
    writer = csv.writer(output)
    entries = session.query(PhotoModel).all()
    for entry in entries:
        fields = map(lambda x: x if isinstance(x, unicode) else x, entry)
        writer.writerow(fields)

print("Dumping emails..")
with open("emails.csv", "w") as output:
    writer = csv.writer(output)
    entries = session.query(EmailModel).all()
    for entry in entries:
        fields = map(lambda x: x if isinstance(x, unicode) else x, entry)
        writer.writerow(fields)

print("Dumping blocked..")
with open("blocked.csv", "w") as output:
    writer = csv.writer(output)
    entries = session.query(BlockedModel).all()
    for entry in entries:
        fields = map(lambda x: x if isinstance(x, unicode) else x, entry)
        writer.writerow(fields)

print("Dumping favorites..")
with open("favorites.csv", "w") as output:
    writer = csv.writer(output)
    entries = session.query(FavoriteModel).all()
    for entry in entries:
        fields = map(lambda x: x if isinstance(x, unicode) else x, entry)
        writer.writerow(fields)

print("Dumping results..")
with open("results.csv", "w") as output:
    writer = csv.writer(output)
    entries = session.query(ResultModel).all()
    for entry in entries:
        fields = map(lambda x: x if isinstance(x, unicode) else x, entry)
        writer.writerow(fields)

print("Dumping admin..")
with open("admin.csv", "w") as output:
    writer = csv.writer(output)
    entries = session.query(AdminModel).all()
    for entry in entries:
        fields = map(lambda x: x if isinstance(x, unicode) else x, entry)
        writer.writerow(fields)
