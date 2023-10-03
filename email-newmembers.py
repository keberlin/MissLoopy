import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import search
from database import MISSLOOPY_DB_URI, db
from emails import *
from localization import *
from model import *
from utils import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

since = db.session.query(AdminModel.last_new_member_search).scalar()

now = datetime.datetime.utcnow()

results = {}

entries = db.session.query(ProfileModel).filter(ProfileModel.verified.is_(True)).filter(ProfileModel.created2>=since).all()
for entry in entries:
  id               = entry.id
  name             = entry.name
  email            = entry.email
  dob              = entry.dob
  location         = entry.location
  x                = entry.x
  y                = entry.y
  tz               = entry.tz
  gender           = entry.gender
  age              = Age(entry.dob)
  ethnicity        = entry.ethnicity
  height           = entry.height
  weight           = entry.weight
  gender_choice    = entry.gender_choice
  age_min          = entry.age_min
  age_max          = entry.age_max
  ethnicity_choice = entry.ethnicity_choice
  height_min       = entry.height_min
  height_max       = entry.height_max
  weight_choice    = entry.weight_choice

  distance = 50
  ids = search.search2(distance,'distance',id,x,y,tz,gender,age,ethnicity,height,weight,gender_choice,age_min,age_max,ethnicity_choice,height_min,height_max,weight_choice)

  # Remove blocked members
  ids = filter(lambda x:not BlockedMutually(id,x), ids)

  for id2 in ids:
    if id2 not in results:
      results[id2] = []
    results[id2].append(id)

for id in results.keys():
  entry = db.session.query(ProfileModel).filter(ProfileModel.id==id).one_or_none()
  if not entry:
    continue
  if not entry.notifications & NOT_NEW_MEMBERS:
    EmailNewMembers(entry, results[id])

db.session.query(AdminModel).update({"last_new_member_search":now},synchronize_session=False)
db.session.commit()
