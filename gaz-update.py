import argparse
import csv
import datetime

from database import db_init, GAZETTEER_DB_URI
from gazetteer import *
from model import LocationModel
from utils import *

parser = argparse.ArgumentParser(description="Create Geographical Gazetteer Information Database.")
parser.add_argument("file", nargs="+", help="a geographical file")
args = parser.parse_args()

session = db_init(GAZETTEER_DB_URI)

# Load locations data

countries = set()
count = added = updated = 0
for file in args.file:
    print("Processing", file)
    with open(file, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";", quoting=csv.QUOTE_NONE, skipinitialspace=True)
        for row in reader:
            count += 1
            location = row[0]
            countries.add(GazCountry(location))
            x = int(row[1])
            y = int(row[2])
            tz = row[3]
            population = int(row[4])

            entry = session.query(LocationModel.population).filter(LocationModel.location == location).one_or_none()
            if not entry:
                item = LocationModel(location=location, x=x, y=y, tz=tz, population=population)
                session.add(item)
                session.commit()
                added += 1
                continue

            # If we have a duplicate location then choose the largest population
            if population > entry.population:
                session.query(LocationModel).filter(LocationModel.location == location).update(
                    {"x": x, "y": y, "tz": tz, "population": population}, synchronize_session=False
                )
                session.commit()
                updated += 1
                continue

# TODO Remove any entries which are no longer valid?

print("Locations : %5d, added %d, updated %d" % (count, added, updated))
print("Countries : %5d" % (len(countries)))
