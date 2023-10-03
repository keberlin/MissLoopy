import logging
import math
import os
import re

from sqlalchemy.sql.expression import or_

from database import db
from gazetteer import *
from mlutils import *
from model import *
from tzone import *
from utils import *


def search2(distance,order,id,x,y,tz,gender,age,ethnicity,height,weight,gender_choice,age_min,age_max,ethnicity_choice,height_min,height_max,weight_choice):
  adjust = GazLatAdjust(y)

  query = db.session.query(ProfileModel.id,ProfileModel.x,ProfileModel.y).filter(ProfileModel.verified.is_(True))

  # Limit profiles to those with genuine locations!
  #rules.append('last_ip_country = country')
  # Only list profiles which match this person's selection criteria
  if distance:
    dx = distance*1000/adjust # Distance is stored in the db as metres so *1000
    dy = distance*1000
    query = query.filter(x-dx<=ProfileModel.x,ProfileModel.x<=x+dx)
    query = query.filter(y-dy<=ProfileModel.y,ProfileModel.y<=y+dy)
  if gender_choice:
    query = query.filter(ProfileModel.gender.op('&')(gender_choice)!=0)
  if age_min:
    now = datetime.datetime.utcnow()
    ref = Datetime(now, tz)
    try:
      dob = datetime.date(ref.year-age_min,ref.month,ref.day)
    except ValueError:
      # cater for leap year
      dob = datetime.date(ref.year-age_min,ref.month,ref.day-1)
    query = query.filter(ProfileModel.dob <= dob)
  if age_max:
    now = datetime.datetime.utcnow()
    ref = Datetime(now, tz)
    try:
      dob = datetime.date(ref.year-age_max-1,ref.month,ref.day)
    except ValueError:
      # cater for leap year
      dob = datetime.date(ref.year-age_max-1,ref.month,ref.day-1)
    query = query.filter(ProfileModel.dob > dob)
  if ethnicity_choice:
    query = query.filter(ProfileModel.ethnicity.op('&')(ethnicity_choice)!=0)
  if height_min:
    query = query.filter(or_(ProfileModel.height.is_(None),ProfileModel.height >= height_min))
  if height_max:
    query = query.filter(or_(ProfileModel.height.is_(None),ProfileModel.height <= height_max))
  if weight_choice:
    query = query.filter(or_(ProfileModel.weight.is_(None),ProfileModel.weight.op('&')(weight_choice) != 0))

  # Only list profiles which match the other member's selection criteria
  query = query.filter(or_(ProfileModel.gender_choice.is_(None),ProfileModel.gender_choice.op('&')(gender)!=0))
  query = query.filter(or_(ProfileModel.age_min.is_(None),ProfileModel.age_min <= age))
  query = query.filter(or_(ProfileModel.age_max.is_(None),ProfileModel.age_max >= age))
  if ethnicity:
    query = query.filter(or_(ProfileModel.ethnicity_choice.is_(None),ProfileModel.ethnicity_choice.op('&')(ethnicity)!=0))
  if height:
    query = query.filter(or_(ProfileModel.height_min.is_(None),ProfileModel.height_min <= height))
    query = query.filter(or_(ProfileModel.height_max.is_(None),ProfileModel.height_max >= height))
  if weight:
    query = query.filter(or_(ProfileModel.weight_choice.is_(None),ProfileModel.weight_choice.op('&')(weight)!=0))
  if order:
    if order == 'age':
      query = query.order_by(ProfileModel.dob.desc())
    elif order == 'login':
      query = query.order_by(ProfileModel.last_login.desc())
    elif order == 'created':
      query = query.order_by(ProfileModel.created2.desc())
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
