import math, itertools

import database, mask

from utils import *
from units import *
from tzone import *
from gazetteer import *
from mlutils import *

db = database.Database(MISS_LOOPY_DB)

def ListMember(id,active,location,x,y,tz,unit_distance):
  db.execute('SELECT * FROM profiles WHERE id=%d LIMIT 1' % (id))
  entry = db.fetchone()
  if not entry:
    return None
  adjust = GazLatAdjust(y)
  dx = abs(x-entry[COL_X])*adjust/1000
  dy = abs(y-entry[COL_Y])/1000
  distance = math.sqrt((dx*dx)+(dy*dy))
  member = {}
  member['id']            = id
  member['image']         = PhotoFilename(MasterPhoto(entry[COL_ID]))
  member['name']          = mask.MaskEverything(entry[COL_NAME])
  member['gender']        = Gender(entry[COL_GENDER])
  member['age']           = Age(entry[COL_DOB])
  member['starsign']      = Starsign(entry[COL_DOB])
  member['ethnicity']     = Ethnicity(entry[COL_ETHNICITY])
  member['location']      = GazPlacename(entry[COL_LOCATION], location)
  member['country']       = GazCountry(entry[COL_LOCATION])
  member['summary']       = mask.MaskEverything(entry[COL_SUMMARY])
  member['last_login']    = Since(entry[COL_LAST_LOGIN])
  member['login_country'] = entry[COL_LAST_IP_COUNTRY]
  member['created']       = Datetime(entry[COL_CREATED2], tz).strftime('%x')
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
