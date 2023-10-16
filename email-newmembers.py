import datetime

from database import db_init, MISSLOOPY_DB_URI
from emails import *
from localization import *
from model import *
import search
from utils import *

session = db_init(MISSLOOPY_DB_URI)

since = session.query(AdminModel.last_new_member_search).scalar()

now = datetime.datetime.utcnow()

results = {}

entries = (
    session.query(ProfileModel).filter(ProfileModel.verified.is_(True)).filter(ProfileModel.created2 >= since).all()
)
for entry in entries:
    id = entry.id
    name = entry.name
    email = entry.email
    dob = entry.dob
    location = entry.location
    x = entry.x
    y = entry.y
    tz = entry.tz
    gender = entry.gender
    age = Age(entry.dob)
    ethnicity = entry.ethnicity
    height = entry.height
    weight = entry.weight
    gender_choice = entry.gender_choice
    age_min = entry.age_min
    age_max = entry.age_max
    ethnicity_choice = entry.ethnicity_choice
    height_min = entry.height_min
    height_max = entry.height_max
    weight_choice = entry.weight_choice

    distance = 50
    entries = search.search2(
        distance,
        "distance",
        id,
        x,
        y,
        tz,
        gender,
        age,
        ethnicity,
        height,
        weight,
        gender_choice,
        age_min,
        age_max,
        ethnicity_choice,
        height_min,
        height_max,
        weight_choice,
    )

    for entry2 in entries:
        if entry2 not in results:
            results[entry2] = []
        results[entry2].append(entry)

for entry, members in results.items():
    if not entry.notifications & NOT_NEW_MEMBERS:
        EmailNewMembers(entry, members)

session.query(AdminModel).update({"last_new_member_search": now}, synchronize_session=False)
session.commit()
