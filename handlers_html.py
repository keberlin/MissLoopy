import datetime, json
import database, search, spam, mask

from utils import *
from units import *
from localization import *
from gazetteer import *
from mlutils import *
from mlparse import *
from mllist import *

db = database.Database(MISS_LOOPY_DB)

# HTML Pages

def handle_index(entry,values):
  # Get most favorite male members
  db.execute('SELECT f.id_favorite,COUNT(DISTINCT f.id) FROM favorites AS f INNER JOIN profiles AS p ON f.id_favorite=p.id WHERE p.gender=1 GROUP BY f.id_favorite ORDER BY COUNT(DISTINCT f.id) DESC LIMIT 2')
  male = map(lambda x:x[0], db.fetchall())

  # Get most favorite female members
  db.execute('SELECT f.id_favorite,COUNT(DISTINCT f.id) FROM favorites AS f INNER JOIN profiles AS p ON f.id_favorite=p.id WHERE p.gender=2 GROUP BY f.id_favorite ORDER BY COUNT(DISTINCT f.id) DESC LIMIT 2')
  female = map(lambda x:x[0], db.fetchall())

  ids = [female[0], male[0], female[1], male[1]]

  entries = []
  db.execute('SELECT id, name, location FROM profiles WHERE id IN (%s)' % (','.join(map(lambda x:str(x), ids))))
  for entry in db.fetchall():
    d = {}
    d['id']      = entry[0]
    d['image']   = PhotoFilename(MasterPhoto(entry[0]))
    filename = os.path.join(BASE_DIR, 'static', d['image'])
    d['size']    = ImageDimensions(filename)
    d['name']    = entry[1]
    d['country'] = GazCountry(entry[2])
    entries.append(d)

  dict = {}
  dict['entries'] = entries

  return dict

def handle_register(entry,values):
  dict = {}
  today = datetime.date.today()
  dict['dob_max'] = datetime.date(today.year-AGE_MIN,today.month,today.day)

  return dict

def handle_profile(entry,values):
  id       = entry[COL_ID]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)

  unit_distance, unit_height = Units(country)

  dict = {}
  dict['name']        = entry[COL_NAME]
  dict['location']    = entry[COL_LOCATION]
  dict['gender']      = entry[COL_GENDER]
  dict['ethnicity']   = entry[COL_ETHNICITY]
  dict['height']      = Height(entry[COL_HEIGHT],unit_height,2)
  dict['weight']      = entry[COL_WEIGHT] or 0
  dict['education']   = entry[COL_EDUCATION] or 0
  dict['status']      = entry[COL_STATUS] or 0
  dict['smoking']     = entry[COL_SMOKING] or 0
  dict['drinking']    = entry[COL_DRINKING] or 0
  dict['occupation']  = entry[COL_OCCUPATION]
  dict['summary']     = entry[COL_SUMMARY]
  dict['description'] = entry[COL_DESCRIPTION]

  return dict

def handle_photos(entry,values):
  id       = entry[COL_ID]

  pids = []
  master = 0
  db.execute('SELECT pid,master FROM photos WHERE id=%d' % (id))
  for entry in db.fetchall():
    pids.append(entry[0])
    if entry[1]:
      master = entry[0]

  dict = {}
  dict['id']     = id
  dict['pids']   = pids
  dict['master'] = master

  return dict

def handle_seeking(entry,values):
  id       = entry[COL_ID]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)

  unit_distance, unit_height = Units(country)

  dict = {}
  dict['gender_choice']    = entry[COL_GENDER_CHOICE] or 0
  dict['ethnicity_choice'] = entry[COL_ETHNICITY_CHOICE] or 0
  dict['weight_choice']    = entry[COL_WEIGHT_CHOICE] or 0
  dict['age_min']          = entry[COL_AGE_MIN]
  dict['age_max']          = entry[COL_AGE_MAX]
  dict['height_min']       = Height(entry[COL_HEIGHT_MIN],unit_height,2)
  dict['height_max']       = Height(entry[COL_HEIGHT_MAX],unit_height,2)
  dict['looking_for']      = entry[COL_LOOKING_FOR]

  return dict

def handle_matches(entry,values):
  MAX_MATCHES = 100

  id               = entry[COL_ID]
  location         = entry[COL_LOCATION]
  country          = GazCountry(location)
  x                = entry[COL_X]
  y                = entry[COL_Y]
  tz               = entry[COL_TZ]
  gender           = entry[COL_GENDER]
  age              = Age(entry[COL_DOB])
  ethnicity        = entry[COL_ETHNICITY]
  height           = entry[COL_HEIGHT]
  weight           = entry[COL_WEIGHT]
  gender_choice    = entry[COL_GENDER_CHOICE]
  age_min          = entry[COL_AGE_MIN]
  age_max          = entry[COL_AGE_MAX]
  ethnicity_choice = entry[COL_ETHNICITY_CHOICE]
  height_min       = entry[COL_HEIGHT_MIN]
  height_max       = entry[COL_HEIGHT_MAX]
  weight_choice    = entry[COL_WEIGHT_CHOICE]

  ids = search.search2(300,'distance',id,x,y,tz,gender,age,ethnicity,height,weight,gender_choice,age_min,age_max,ethnicity_choice,height_min,height_max,weight_choice)[:MAX_MATCHES]

  # Remove blocked members
  ids = filter(lambda x:not BlockedMutually(id,x), ids)

  SaveResults(id, ids)

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  criteria = []
  if gender_choice:
    criteria.append('%s' % (GenderList(gender_choice)))
  if age_min or age_max:
    criteria.append('%s years old' % (Range(age_min, age_max)))
  if height_min or height_max:
    criteria.append('%s tall' % (Range(Height(height_min,unit_height,2), Height(height_max,unit_height,2))))
  if ethnicity_choice:
    criteria.append('%s' % (EthnicityList(ethnicity_choice)))

  dict = {}
  dict['action']   = 'member'
  dict['type']     = 'short'
  dict['criteria'] = ', '.join(criteria)
  dict['entries']  = ListMembers(ids,None,location,x,y,tz,unit_distance)

  return dict

def handle_search(entry,values):
  id       = entry[COL_ID]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)

  unit_distance, unit_height = Units(country)

  dict = {}
  dict['location'] = location
  dict['metric']   = unit_distance == UNIT_KM

  return dict

def handle_results(entry,values):
  MAX_MATCHES = 200

  id               = entry[COL_ID]
  location         = entry[COL_LOCATION]
  country          = GazCountry(location)
  x                = entry[COL_X]
  y                = entry[COL_Y]
  tz               = entry[COL_TZ]
  gender           = entry[COL_GENDER]
  age              = Age(entry[COL_DOB])
  ethnicity        = entry[COL_ETHNICITY]
  height           = entry[COL_HEIGHT]
  weight           = entry[COL_WEIGHT]
  gender_choice    = entry[COL_GENDER_CHOICE]
  age_min          = entry[COL_AGE_MIN]
  age_max          = entry[COL_AGE_MAX]
  ethnicity_choice = entry[COL_ETHNICITY_CHOICE]
  height_min       = entry[COL_HEIGHT_MIN]
  height_max       = entry[COL_HEIGHT_MAX]
  weight_choice    = entry[COL_WEIGHT_CHOICE]

  ParseAge(values, 'age_min')
  ParseAge(values, 'age_max')
  ParseRange(values, 'age_min', 'age_max')
  ParseHeight(values, 'height_min')
  ParseHeight(values, 'height_max')
  ParseRange(values, 'height_min', 'height_max')

  distance = None
  if values.get('distance'):
    distance = int(values['distance'])
    search_location = location
    if values.get('location'):
      tuple = GazLocation(values['location'])
      if tuple:
        search_location = values['location']
        x = tuple[0]
        y = tuple[1]
  if values.get('age_min'):
    age_min = int(values['age_min'])
  if values.get('age_max'):
    age_max = int(values['age_max'])
  if values.get('ethnicity_choice'):
    ethnicity_choice = eval(values['ethnicity_choice'])
  if values.get('height_min'):
    height_min = int(values['height_min'])
  if values.get('height_max'):
    height_max = int(values['height_max'])
  if values.get('weight_choice'):
    weight_choice = eval(values['weight_choice'])
  order = None
  if values.get('order'):
    order = values['order']

  ids = search.search2(distance,order,id,x,y,tz,gender,age,ethnicity,height,weight,gender_choice,age_min,age_max,ethnicity_choice,height_min,height_max,weight_choice)[:MAX_MATCHES]

  # Remove blocked members
  ids = filter(lambda x:not BlockedMutually(id,x), ids)

  SaveResults(id, ids)

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  criteria = []
  if gender_choice:
    criteria.append('%s' % (GenderList(gender_choice)))
  if age_min or age_max:
    criteria.append('%s years old' % (Range(age_min, age_max)))
  if height_min or height_max:
    criteria.append('%s tall' % (Range(Height(height_min,unit_height,2), Height(height_max,unit_height,2))))
  if ethnicity_choice:
    criteria.append('%s' % (EthnicityList(ethnicity_choice)))

  dict = {}
  dict['action']   = 'member'
  dict['type']     = 'short'
  dict['around']   = Distance(distance,unit_distance) + ' around ' + GazPlacename(search_location, location) if distance else 'Worldwide'
  dict['criteria'] = ', '.join(criteria)
  dict['entries']  = ListMembers(ids,None,location,x,y,tz,unit_distance)
  dict['nav']      = 'search'

  return dict

def handle_member(entry,values):
  if not values.get('id'):
    return {'error': 'id not specified'}

  id_view = int(values['id'])

  id       = entry[COL_ID]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)
  x        = entry[COL_X]
  y        = entry[COL_Y]
  tz       = entry[COL_TZ]

  dict = {}
  dict['id']          = id_view
  dict['id_previous'] = PreviousResult(id, id_view)
  dict['id_next']     = NextResult(id, id_view)

  db.execute('SELECT * FROM profiles WHERE verified AND id=%d LIMIT 1' % (id_view))
  entry = db.fetchone()
  if not entry:
    dict['error'] = "This member doesn't exist or has removed their account."
    return dict

  dict['name'] = mask.MaskEverything(entry[COL_NAME])

  if Blocked(id_view, id):
    dict['error'] = 'This member has blocked you.'
    return dict

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  location = entry[COL_LOCATION]

  dict['mylat']          = y*360.0/CIRCUM_Y
  dict['mylng']          = x*360.0/CIRCUM_X
  # About me
  dict['gender']         = Gender(entry[COL_GENDER])
  dict['age']            = Age(entry[COL_DOB])
  dict['starsign']       = Starsign(entry[COL_DOB])
  dict['ethnicity']      = Ethnicity(entry[COL_ETHNICITY])
  dict['location']       = entry[COL_LOCATION]
  dict['country']        = GazCountry(entry[COL_LOCATION])
  dict['lat']            = entry[COL_Y]*360.0/CIRCUM_Y
  dict['lng']            = entry[COL_X]*360.0/CIRCUM_X
  dict['height']         = Height(entry[COL_HEIGHT],unit_height,2)
  dict['weight']         = Weight(entry[COL_WEIGHT])
  dict['education']      = Education(entry[COL_EDUCATION])
  dict['status']         = Status(entry[COL_STATUS])
  dict['smoking']        = Smoking(entry[COL_SMOKING])
  dict['drinking']       = Drinking(entry[COL_DRINKING])
  dict['summary']        = mask.MaskEverything(entry[COL_SUMMARY])
  dict['occupation']     = mask.MaskEverything(entry[COL_OCCUPATION])
  dict['description']    = mask.MaskEverything(entry[COL_DESCRIPTION])
  dict['last_login']     = Since(entry[COL_LAST_LOGIN])
  dict['login_country']  = entry[COL_LAST_IP_COUNTRY]
  dict['created']        = Datetime(entry[COL_CREATED2],tz).strftime('%x')
  # Seeking
  dict['gender_choice']  = GenderList(entry[COL_GENDER_CHOICE])
  dict['age_range']      = Range(entry[COL_AGE_MIN], entry[COL_AGE_MAX])
  dict['looking_for']    = mask.MaskEverything(entry[COL_LOOKING_FOR])

  master = MasterPhoto(id_view)
  dict['image'] = PhotoFilename(master)
  pids = []
  db.execute('SELECT pid FROM photos WHERE id=%d' % (id_view))
  for entry in db.fetchall():
    pid = entry[0]
    if pid != master:
      pids.append(pid)
  dict['images'] = []
  for pid in pids:
    dict['images'].append(PhotoFilename(pid))

  return dict

def handle_emailthread2(entry,values):
  return handle_emailthread(entry,values)

def handle_emailthread(entry,values):
  if not values.get('id'):
    return {'error': 'id not specified'}

  id_with = int(values['id'])

  id       = entry[COL_ID]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)
  x        = entry[COL_X]
  y        = entry[COL_Y]
  tz       = entry[COL_TZ]

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  dict = {}
  dict['id']          = id_with
  dict['id_previous'] = PreviousResult(id, id_with)
  dict['id_next']     = NextResult(id, id_with)

  db.execute('SELECT * FROM profiles WHERE verified AND id=%d LIMIT 1' % (id_with))
  entry = db.fetchone()
  if not entry:
    dict['error'] = "This member doesn't exist or has removed their account."
    return dict

  dict['entry'] = ListMember(id_with,0,location,x,y,tz,unit_distance)
  dict['name']  = mask.MaskEverything(entry[COL_NAME])

  if Blocked(id_with, id):
    dict['error'] = 'This member has blocked you.'
    return dict

  spammer = spam.AnalyseSpammer(id_with)

  SetLocale(country)

  image = PhotoFilename(MasterPhoto(id_with))
  emails = []
  db.execute('SELECT * FROM emails WHERE (id_from=%d AND id_to=%d) OR (id_from=%d AND id_to=%d) ORDER BY sent DESC' % (id, id_with, id_with, id))
  for entry in db.fetchall():
    d = {}
    d['sent']     = entry[COL4_ID_FROM] == id
    d['message']  = entry[COL4_MESSAGE]
    d['is_image'] = d['message'].startswith('data:image/')
    d['time']     = Since(entry[COL4_SENT], False)
    d['viewed']   = entry[COL4_VIEWED]
    if not d['sent'] and not d['is_image']:
      d['id_with'] = id_with
      d['image']   = image
      d['spam']    = spam.IsSpamFactored(spam.AnalyseSpam(d['message']), spammer, 2)
      d['message'] = mask.MaskEverything(d['message'])
    emails.append(d)
  dict['entries'] = emails

  db.execute('UPDATE emails SET viewed=1 WHERE id_from=%d AND id_to=%d' % (id_with, id))
  db.commit()

  return dict

def handle_inbox(entry,values):
  id       = entry[COL_ID]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)
  x        = entry[COL_X]
  y        = entry[COL_Y]
  tz       = entry[COL_TZ]

  db.execute('SELECT DISTINCT id_from FROM emails WHERE id_to=%d ORDER BY sent DESC' % (id))
  ids = map(lambda x:x[0], db.fetchall())

  # Remove blocked members
  ids = filter(lambda x:not BlockedMutually(id,x), ids)

  SaveResults(id, ids)

  counts = []
  for id_from in ids:
    db.execute('SELECT COUNT(*) FROM emails WHERE id_from=%d and id_to=%d and viewed=0' % (id_from, id))
    entry = db.fetchone()
    counts.append(entry[0])

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  dict = {}
  dict['action']  = 'emailthread'
  dict['type']    = 'number'
  dict['entries'] = ListMembers(ids,counts,location,x,y,tz,unit_distance)

  return dict

def handle_outbox(entry,values):
  id       = entry[COL_ID]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)
  x        = entry[COL_X]
  y        = entry[COL_Y]
  tz       = entry[COL_TZ]

  db.execute('SELECT DISTINCT id_to FROM emails WHERE id_from=%d ORDER BY sent DESC' % (id))
  ids = map(lambda x:x[0], db.fetchall())

  # Remove blocked members
  ids = filter(lambda x:not BlockedMutually(id,x), ids)

  SaveResults(id, ids)

  counts = []
  for id_to in ids:
    db.execute('SELECT COUNT(*) FROM emails WHERE id_from=%d and id_to=%d and viewed=0' % (id, id_to))
    entry = db.fetchone()
    counts.append(entry[0])

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  dict = {}
  dict['action']  = 'emailthread'
  dict['type']    = 'number'
  dict['entries'] = ListMembers(ids,counts,location,x,y,tz,unit_distance)

  return dict

def handle_favorites(entry,values):
  id       = entry[COL_ID]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)
  x        = entry[COL_X]
  y        = entry[COL_Y]
  tz       = entry[COL_TZ]

  db.execute('SELECT DISTINCT f.id_favorite FROM favorites AS f INNER JOIN profiles AS p ON f.id_favorite=p.id WHERE f.id=%d ORDER BY p.last_login DESC' % (id))
  ids = map(lambda x:x[0], db.fetchall())

  # Remove blocked members
  ids = filter(lambda x:not BlockedMutually(id,x), ids)

  SaveResults(id, ids)

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  dict = {}
  dict['action']  = 'member'
  dict['type']    = 'full'
  dict['entries'] = ListMembers(ids,None,location,x,y,tz,unit_distance)

  return dict

def handle_blocked(entry,values):
  id       = entry[COL_ID]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)
  x        = entry[COL_X]
  y        = entry[COL_Y]
  tz       = entry[COL_TZ]

  db.execute('SELECT DISTINCT id_block FROM blocked WHERE id=%d' % (id))
  ids = map(lambda x:x[0], db.fetchall())

  SaveResults(id, ids)

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  dict = {}
  dict['action']  = 'member'
  dict['type']    = 'full'
  dict['entries'] = ListMembers(ids,None,location,x,y,tz,unit_distance)

  return dict

def handle_account(entry,values):
  id       = entry[COL_ID]
  email    = entry[COL_EMAIL]
  password = entry[COL_PASSWORD]
  dob      = entry[COL_DOB]

  dict = {}
  dict['email']    = email
  dict['password'] = password
  dict['dob']      = dob

  return dict

def handle_verify(entry,values):
  if not values.get('id'):
    return {'error': 'id not specified'}
  if not values.get('email'):
    return {'error': 'email not specified'}

  id    = int(values['id'])
  email = values['email']

  db.execute('SELECT id FROM profiles WHERE email LIKE %s LIMIT 1' % (Quote(email)))
  entry = db.fetchone()
  if not entry:
    return {'error': 'Email address not found'}
  if entry[0] != id:
    return {'error': 'Id does not match'}

  now = datetime.datetime.now()
  db.execute('UPDATE profiles SET created2=%s, verified=1 WHERE id=%d AND not verified' % (Quote(str(now)), id))
  db.commit()

  return {}

def handle_cancelled(entry,values):
  id = entry[COL_ID]

  DeleteMember(id)

  return {}
