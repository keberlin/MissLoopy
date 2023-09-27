import os, math, logging, re
from sqlalchemy.sql.expression import or_

from utils import *
from tzone import *
from gazetteer import *
from mlutils import *

from database import db
from model import *

def search2(distance,order,id,x,y,tz,gender,age,ethnicity,height,weight,gender_choice,age_min,age_max,ethnicity_choice,height_min,height_max,weight_choice):
  adjust = GazLatAdjust(y)

  query = db.session.query(ProfilesModel.id,ProfilesModel.x,ProfilesModel.y).filter(ProfilesModel.verified.is_(True))

  # Limit profiles to those with genuine locations!
  #rules.append('last_ip_country = country')
  # Only list profiles which match this person's selection criteria
  if distance:
    dx = distance*1000/adjust # Distance is stored in the db as metres so *1000
    dy = distance*1000
    query = query.filter(x-dx<=ProfilesModel.x,ProfilesModel.x<=x+dx)
    query = query.filter(y-dy<=ProfilesModel.y,ProfilesModel.y<=y+dy)
  if gender_choice:
    query = query.filter(ProfilesModel.gender.op('&')(gender_choice)!=0)
  if age_min:
    now = datetime.datetime.utcnow()
    ref = Datetime(now, tz)
    try:
      dob = datetime.date(ref.year-age_min,ref.month,ref.day)
    except ValueError:
      # cater for leap year
      dob = datetime.date(ref.year-age_min,ref.month,ref.day-1)
    query = query.filter(ProfilesModel.dob <= dob)
  if age_max:
    now = datetime.datetime.utcnow()
    ref = Datetime(now, tz)
    try:
      dob = datetime.date(ref.year-age_max-1,ref.month,ref.day)
    except ValueError:
      # cater for leap year
      dob = datetime.date(ref.year-age_max-1,ref.month,ref.day-1)
    query = query.filter(ProfilesModel.dob > dob)
  if ethnicity_choice:
    query = query.filter(ProfilesModel.ethnicity.op('&')(ethnicity_choice)!=0)
  if height_min:
    query = query.filter(or_(ProfilesModel.height.is_(None),ProfilesModel.height >= height_min))
  if height_max:
    query = query.filter(or_(ProfilesModel.height.is_(None),ProfilesModel.height <= height_max))
  if weight_choice:
    query = query.filter(or_(ProfilesModel.weight.is_(None),ProfilesModel.weight.op('&')(weight_choice) != 0))

  # Only list profiles which match the other member's selection criteria
  query = query.filter(or_(ProfilesModel.gender_choice.is_(None),ProfilesModel.gender_choice.op('&')(gender)!=0))
  query = query.filter(or_(ProfilesModel.age_min.is_(None),ProfilesModel.age_min <= age))
  query = query.filter(or_(ProfilesModel.age_max.is_(None),ProfilesModel.age_max >= age))
  if ethnicity:
    query = query.filter(or_(ProfilesModel.ethnicity_choice.is_(None),ProfilesModel.ethnicity_choice.op('&')(ethnicity)!=0))
  if height:
    query = query.filter(or_(ProfilesModel.height_min.is_(None),ProfilesModel.height_min <= height))
    query = query.filter(or_(ProfilesModel.height_max.is_(None),ProfilesModel.height_max >= height))
  if weight:
    query = query.filter(or_(ProfilesModel.weight_choice.is_(None),ProfilesModel.weight_choice.op('&')(weight)!=0))
  if order:
    if order == 'age':
      query = query.order_by(ProfilesModel.dob.desc())
    elif order == 'login':
      query = query.order_by(ProfilesModel.last_login.desc())
    elif order == 'created':
      query = query.order_by(ProfilesModel.created2.desc())
    else:
      pass # Order must be by distance

  entries = query.all()

  list = []
  for entry in entries:
    id = entry.id
    dx = abs(x-entry.x)*adjust/1000
    dy = abs(y-entry.y)/1000
    d = math.sqrt((dx*dx)+(dy*dy))
    if distance and d > distance:
      continue
    list.append((id,d))
  if order == 'distance':
    list.sort(cmp=lambda a,b:int(a[1]-b[1])) # TODO

  return [x[0] for x in list]
