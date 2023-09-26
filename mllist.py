import math, itertools

import mask

from utils import *
from units import *
from tzone import *
from gazetteer import *
from mlutils import *
from database import db
from model import *

def ListMember(id,active,location,x,y,tz,unit_distance):
  entry = db.session.query(ProfilesModel).filter(ProfilesModel.id==id).one_or_none()
  if not entry:
    return None
  adjust = GazLatAdjust(y)
  dx = abs(x-entry.x)*adjust/1000
  dy = abs(y-entry.y)/1000
  distance = math.sqrt((dx*dx)+(dy*dy))

  member = {}
  member['id']            = id
  member['image']         = PhotoFilename(MasterPhoto(entry.id))
  member['name']          = mask.MaskEverything(entry.name)
  member['gender']        = Gender(entry.gender)
  member['age']           = Age(entry.dob)
  member['starsign']      = Starsign(entry.dob)
  member['ethnicity']     = Ethnicity(entry.ethnicity)
  member['location']      = GazPlacename(entry.location, location)
  member['country']       = GazCountry(entry.location)
  member['summary']       = mask.MaskEverything(entry.summary)
  member['last_login']    = Since(entry.last_login)
  member['login_country'] = entry.last_ip_country
  member['created']       = Datetime(entry.created2, tz).strftime('%x')
  member['distance']      = Distance(distance, unit_distance)
  member['active']        = active

  return member

def ListMembers(ids,counts,location,x,y,tz,unit_distance):
  members = []
  for id, count in itertools.izip_longest(ids,counts if counts else []):
    member = ListMember(id,count,location,x,y,tz,unit_distance)
    if not member:
      continue
    members.append(member)
  return members
