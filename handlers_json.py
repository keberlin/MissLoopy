import os, re, datetime, io, cStringIO, base64, psycopg2, time

from PIL import Image

import database, search, spam, mask

from utils import *
from units import *
from localization import *
from gazetteer import *
from emails import *
from mlutils import *
from mlparse import *
from mlemail import *

from logger import *

BASE_DIR = os.path.dirname(__file__)

db = database.Database(MISS_LOOPY_DB)

MAX_MATCHES = 8
MAX_LENGTH = 3000

# JSON returns

def handle_closestnames(entry,values,files):
  MAX_MATCHES = 5

  if not values.get('query'):
    return {'error': 'No query specified.'}

  query = values['query'].lstrip()

  closest = GazClosestMatchesQuick(query, MAX_MATCHES)

  return {'matches': closest}

def handle_mlaccount(entry,values,files):
  if not values.get('password'):
    return {'error': 'No Password specified.'}

  id = entry[COL_ID]

  # TODO Find a mechanism for updating a member's email address too..
  attributes = ['password']

  attrs = {}
  for attr in values:
    if not attr in attributes:
      continue
    if not values.get(attr):
      continue
    if attr.endswith('_choice'):
      attrs[attr] = values[attr]
    else:
      attrs[attr] = Quote(values[attr][:MAX_LENGTH])
  for attr in attributes:
    if attr in attrs:
      continue
    attrs[attr] = 'Null'

  db.execute('UPDATE profiles SET %s WHERE id=%d' % (','.join([(attr+'='+value) for attr,value in attrs.iteritems()]), id))
  db.commit()

  return {'message': 'Account updated successfully.'}

def handle_mladdfavorite(entry,values,files):
  id = entry[COL_ID]

  ids = map(lambda x:int(x), values['id'].split('|'))

  for id_favorite in ids:
    db.execute('INSERT INTO favorites (id,id_favorite) VALUES (%d,%d)' % (id, id_favorite))
  db.commit()

  if len(ids) == 1:
    return {'message': 'This member has been added to your favorites list.'}
  else:
    return {'message': 'These members have been added to your favorites list.'}

def handle_mlblock(entry,values,files):
  id = entry[COL_ID]

  ids = map(lambda x:int(x), values['id'].split('|'))

  for id_block in ids:
    db.execute('INSERT INTO blocked (id,id_block) VALUES (%d,%d)' % (id, id_block))
  db.commit()

  if len(ids) == 1:
    return {'message': 'This member has now been blocked.'}
  else:
    return {'message': 'These members have now been blocked.'}

def handle_mldeletefavorite(entry,values,files):
  id = entry[COL_ID]

  if 'ids' in values: ids = values['ids']
  else: ids = map(lambda x:int(x), values['id'].split('|'))

  for id_favorite in ids:
    db.execute('DELETE FROM favorites WHERE id=%d AND id_favorite=%d' % (id, id_favorite))
  db.commit()

  if len(ids) == 1:
    return {'message': 'This member has been removed from your favorites list.'}
  else:
    return {'message': 'These members have been removed from your favorites list.'}

def handle_mldeletephoto(entry,values,files):
  id = entry[COL_ID]

  if 'pids' in values: pids = values['pids']
  else: pids = map(lambda x:int(x), values['pid'].split('|'))

  for pid in pids:
    # Ensure this member owns the photo first
    db.execute('SELECT id FROM photos WHERE pid=%d LIMIT 1' % (pid))
    entry = db.fetchone()
    if not entry:
      return {'error': 'Photo %d not found.' % (pid)}
    if entry[0] != id:
      return {'error': 'You are not the owner of photo %d.' % (pid)}

  DeletePhotos(pids)

  master = MasterPhoto(id)

  if len(pids) == 1:
    return {'message': 'This photo has been deleted.', 'pids': pids, 'master': master}
  else:
    return {'message': 'These photos have been deleted.', 'pids': pids, 'master': master}

def handle_mlmasterphoto(entry,values,files):
  if not values.get('pid'):
    return {'error': 'No Photo selected.'}

  id = entry[COL_ID]

  pid = int(values['pid'])

  # Ensure this member owns the photo first
  db.execute('SELECT COUNT(*) FROM photos WHERE id=%d AND pid=%d' % (id, pid))
  entry = db.fetchone()
  if entry[0] == 0:
    return {'error': 'You are not the owner of this photo.'}
  # Remove the master flag from all photos
  db.execute('UPDATE photos SET master=false WHERE id=%d' % (id))
  # Restore the master flag for the selected photo
  db.execute('UPDATE photos SET master=true WHERE pid=%d' % (pid))
  db.commit()

  return {'message': 'This photo has been set to your main profile photo.', 'master': pid}

def handle_mlpassword(entry,values,files):
  email = values['email']

  # Retrieve the password
  db.execute('SELECT password FROM profiles WHERE email ILIKE %s LIMIT 1' % (Quote(email)))
  entry = db.fetchone()
  if not entry:
    return {'error': 'Email Address not found.'}

  EmailPassword(email,entry[0])

  return {'message': 'Your password reminder has been sent...'}

def handle_mlprofile(entry,values,files):
  if not values.get('name'):
    return {'error': 'No Display Name specified.'}

  id = entry[COL_ID]

  ParseHeight(values, 'height')

  attributes = ['name', 'gender', 'ethnicity', 'height', 'weight', 'education', 'status', 'smoking', 'drinking', 'occupation', 'summary', 'description']

  attrs = {}
  if 'location' in values:
    tuple = GazLocation(values['location'])
    if not tuple:
      return {'matches': GazClosestMatches(values['location'], MAX_MATCHES)}
    attrs['location'] = Quote(values['location'])
    attrs['x'] = str(tuple[0])
    attrs['y'] = str(tuple[1])
    attrs['tz'] = Quote(tuple[2])
  for attr in values:
    if not attr in attributes:
      continue
    if not values.get(attr):
      continue
    if attr.endswith('_choice'):
      attrs[attr] = values[attr]
    else:
      attrs[attr] = Quote(values[attr][:MAX_LENGTH])
  for attr in attributes:
    if attr in attrs:
      continue
    attrs[attr] = 'Null'

  db.execute('UPDATE profiles SET %s WHERE id=%d' % (','.join([(attr+'='+value) for attr,value in attrs.iteritems()]), id))
  db.commit()

  return {'message': 'Profile updated successfully.'}

def handle_mlregister(entry,values,files):
  if not values.get('email'):
    return {'error': 'No Email Address specified.'}
  if not values.get('password'):
    return {'error': 'No Password specified.'}
  if not values.get('dob'):
    return {'error': 'No Date of Birth specified.'}
  if not values.get('name'):
    return {'error': 'No Display Name specified.'}
  if not values.get('gender'):
    return {'error': 'No Gender specified.'}
  if not values.get('ethnicity'):
    return {'error': 'No Ethnicity specified.'}
  if not values.get('gender_choice'):
    return {'error': 'No Seeking gender specified.'}
  if not values.get('location'):
    return {'error': 'No Location specified.'}

  email    = values['email']
  dob      = values['dob']
  location = values['location']

  if not ParseEmail(email):
    return {'error': 'Email Address not valid.'}
  dt = ParseDob(dob)
  if not dt or dt.year < 1900:
    return {'error': 'Date of birth not valid.'}
  age = Age(dt)
  if age<18:
    return {'error': 'Sorry, you\'re too young to register.'}

  db.execute('SELECT COUNT(*) FROM profiles WHERE email ILIKE %s LIMIT 1' % (Quote(email)))
  entry = db.fetchone()
  if entry[0]:
    return {'error': 'Email Address already in use.'}

  attributes = ['email', 'password', 'name', 'gender', 'ethnicity',
                'height', 'weight', 'education', 'status', 'smoking', 'drinking', 'occupation', 'summary', 'description',
                'gender_choice', 'ethnicity_choice', 'age_min', 'age_max', 'height_min', 'height_max', 'weight_choice', 'looking_for']

  attrs = {}
  now = datetime.datetime.utcnow()
  attrs['created2'] = Quote(str(now))
  attrs['dob'] = Quote(dt.strftime('%Y-%m-%d'))
  if 'location' in values:
    tuple = GazLocation(values['location'])
    if not tuple:
      return {'matches': GazClosestMatches(values['location'], MAX_MATCHES)}
    attrs['location'] = Quote(values['location'])
    attrs['x'] = str(tuple[0])
    attrs['y'] = str(tuple[1])
    attrs['tz'] = Quote(tuple[2])
  for attr in values:
    if not attr in attributes:
      continue
    if not values.get(attr):
      continue
    if attr.endswith('_choice'):
      attrs[attr] = values[attr]
    else:
      attrs[attr] = Quote(values[attr][:MAX_LENGTH])
  for attr in attributes:
    if attr in attrs:
      continue
    attrs[attr] = 'Null'

  while True:
    try:
      db.execute('INSERT INTO profiles (%s) VALUES (%s)' % (','.join([(attr) for attr,value in attrs.iteritems()]), ','.join([(value) for attr,value in attrs.iteritems()])))
      id = db.lastval()
      db.commit()
      break
    except psycopg2.IntegrityError as e:
      db.rollback()
      id = db.lastval()
      db.execute('SELECT COUNT(*) FROM profiles WHERE id=%d' % (id))
      entry = db.fetchone()
      if entry[0] == 0:
        logger.error('ERROR: Problem registering %s' % repr(attrs))
        raise e

  EmailVerify(email,id)

  return {'code': 1002}

def handle_mlpassword(entry,values,files):
  if not values.get('email'):
    return {'error': 'No email specified.'}

  email = values['email']

  # Retrieve the password
  db.execute('SELECT password FROM profiles WHERE email ILIKE %s LIMIT 1' % (Quote(email)))
  entry = db.fetchone()
  if not entry:
    return {'error': 'Email Address not found.'}

  EmailPassword(email,entry[0])

  return {'message': 'Your password reminder has been sent...'}

def handle_mlresend(entry,values,files):
  if not values.get('email'):
    return {'error': 'No email specified.'}

  email = values['email']

  # Retrieve the newly created id
  db.execute('SELECT id FROM profiles WHERE email ILIKE %s LIMIT 1' % (Quote(email)))
  entry = db.fetchone()
  if not entry:
    return {'error': 'Account not found.'}

  EmailVerify(email,entry[0])

  return {'message': 'Verify Registration email has been resent...'}

def handle_mlsearch(entry,values,files):
  if not values.get('query'):
    return {'error': 'No query specified.'}

  query = values['query'].strip()

  tuple = GazLocation(query)
  if not tuple:
    return {'matches': GazClosestMatches(query, MAX_MATCHES)}

  return {'code': 1003}

def handle_mlseeking(entry,values,files):
  id = entry[COL_ID]

  if not values.get('gender_choice'):
    return {'error': 'No Seeking Gender specified.'}

  ParseAge(values, 'age_min')
  ParseAge(values, 'age_max')
  ParseRange(values, 'age_min', 'age_max')
  ParseHeight(values, 'height_min')
  ParseHeight(values, 'height_max')
  ParseRange(values, 'height_min', 'height_max')

  attributes = ['gender_choice', 'ethnicity_choice', 'age_min', 'age_max', 'height_min', 'height_max', 'weight_choice', 'looking_for']

  attrs = {}
  for attr in values:
    if not attr in attributes:
      continue
    if not values.get(attr):
      continue
    if attr.endswith('_choice'):
      attrs[attr] = values[attr]
    else:
      attrs[attr] = Quote(values[attr][:MAX_LENGTH])
  for attr in attributes:
    if attr in attrs:
      continue
    attrs[attr] = 'Null'

  db.execute('UPDATE profiles SET %s WHERE id=%d' % (','.join([(attr+'='+value) for attr,value in attrs.iteritems()]), id))
  db.commit()

  return {'message': 'Seeking updated successfully.'}

def handle_mlsendemail(entry,values,files):
  id       = entry[COL_ID]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)
  x        = entry[COL_X]
  y        = entry[COL_Y]
  tz       = entry[COL_TZ]

  if not values.get('message'):
    return {'error': 'No message specified.'}

  id_to   = int(values['id'])
  message = values['message']

  if Blocked(id_to, id):
    return {'error': 'This member has blocked you.'}

  if Blocked(id, id_to):
    return {'error': 'You have blocked this member.'}

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  tuple   = spam.AnalyseSpam(message)
  spammer = spam.AnalyseSpammer(id)
  if spam.IsSpamFactored(tuple, spammer, 2):
    message = re.sub('[\r\n]+',' ',message)
    with open(os.path.join(BASE_DIR, 'junk-auto.log'), 'a') as f:
      f.write('%d %s\n' % (id, message.encode('utf-8')))

  db.execute('SELECT email, notifications FROM profiles WHERE verified AND id=%d LIMIT 1' % (id_to))
  entry = db.fetchone()
  if not entry:
    return {'error': 'This member cannot be found.'}

  email         = entry[0]
  notifications = entry[1]

  now = datetime.datetime.utcnow()
  db.execute('INSERT INTO emails (id_from,id_to,message,sent) VALUES (%d,%d,%s,%s)' % (id, id_to, Quote(message), Quote(str(now))))
  db.commit()

  if not notifications & NOT_NEW_MESSAGE:
    EmailNotify(email, id, x, y, tz, unit_distance)

  d = {}
  d['sent']     = True
  d['message']  = message
  d['is_image'] = False
  d['time']     = Since(now, False)
  d['viewed']   = False

  return {'message': 'Your message has been sent.', 'entry': d}

def handle_mlsendphoto(entry,values,files):
  IMAGE_MAX_SIZE = 400

  id       = entry[COL_ID]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)
  x        = entry[COL_X]
  y        = entry[COL_Y]
  tz       = entry[COL_TZ]

  id_to = int(values['id'])

  if Blocked(id_to, id):
    return {'error': 'This member has blocked you.'}

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  try:
    im = Image.open(files['file'].stream)
  except:
    return {'error': 'Unrecognized image format.'}
  # Ensure it is no bigger than this
  im.thumbnail((IMAGE_MAX_SIZE,IMAGE_MAX_SIZE), Image.ANTIALIAS)
  data = cStringIO.StringIO()
  im.save(data, 'JPEG')
  message = 'data:image/jpg;base64,' + base64.b64encode(data.getvalue())

  db.execute('SELECT email FROM profiles WHERE verified AND id=%d LIMIT 1' % (id_to))
  entry = db.fetchone()
  if not entry:
    return {'error': 'This member cannot be found.'}

  email = entry[0]

  now = datetime.datetime.utcnow()
  db.execute('INSERT INTO emails (id_from,id_to,message,sent) VALUES (%d,%d,%s,%s)' % (id, id_to, Quote(message), Quote(str(now))))
  db.commit()

  EmailNotify(email, id, x, y, tz, unit_distance)

  d = {}
  d['sent']     = True
  d['message']  = message
  d['is_image'] = True
  d['time']     = Since(now, False)
  d['viewed']   = False

  return {'message': 'Your photo has been sent.', 'entry': d}

def handle_mlspam(entry,values,files):
  id = entry[COL_ID]

  id_spam = int(values['id'])

  db.execute("SELECT DISTINCT message FROM emails WHERE id_from=%d AND id_to=%d AND message NOT LIKE 'data:image/%%'" % (id_spam, id))
  for entry in db.fetchall():
    message = re.sub('[\r\n]+',' ',entry[0])
    with open(os.path.join(BASE_DIR, 'junk-reported.log'), 'a') as f:
      f.write('%d %s\n' % (id_spam, message.encode('utf-8')))

  return {'message': 'Thank you for reporting this member...'}

def handle_mlunblock(entry,values,files):
  id = entry[COL_ID]

  if 'ids' in values: ids = values['ids']
  else: ids = map(lambda x:int(x), values['id'].split('|'))

  for id_block in ids:
    db.execute('DELETE FROM blocked WHERE id=%d AND id_block=%d' % (id, id_block))
  db.commit()

  if len(ids) == 1:
    return {'message': 'This member has now been unblocked.'}
  else:
    return {'message': 'These members have now been unblocked.'}

def handle_mluploadphoto(entry,values,files):
  IMAGE_MIN_SIZE = 100
  IMAGE_MAX_SIZE = 600

  id = entry[COL_ID]

  try:
    im = Image.open(files['file'].stream)
  except:
    return {'error': 'Unrecognized image format.'}
  # Ensure it is at least this big
  if im.size[0] < IMAGE_MIN_SIZE or im.size[1] < IMAGE_MIN_SIZE:
    return {'error': 'Photo is too small. It needs to be at least %d by %d pixels.' % (IMAGE_MIN_SIZE, IMAGE_MIN_SIZE)}
  # Ensure it is no bigger than this
  try:
    im.thumbnail((IMAGE_MAX_SIZE,IMAGE_MAX_SIZE), Image.ANTIALIAS)
  except:
    return {'error': 'Unsupported image format.'}

  # Add watermark to bottom-right corner
  if im.mode != 'RGBA':
    try:
      im = im.convert('RGBA')
    except:
      return {'error': 'Unsupported image format.'}
  layer = Image.new('RGBA', im.size, (0,0,0,0))
  mark = Image.open(os.path.join(BASE_DIR, 'watermark.png'))
  layer.paste(mark, (im.size[0]-mark.size[0], im.size[1]-mark.size[1]))
  im = Image.composite(layer, im, layer)

  while True:
    try:
      db.execute('INSERT INTO photos (id) VALUES (%d)' % (id))
      pid = db.lastval()
      db.commit()
      break
    except psycopg2.IntegrityError:
      db.rollback()

  # Create a photo file using pid and copy data into it
  filename = os.path.join(BASE_DIR, 'static', PhotoFilename(pid))
  if os.path.isfile(filename):
    logger.error('ERROR: Photo file %s already exists!' % (filename))
    os.remove(filename)
  im.save(filename, 'JPEG')

  EmailNewPhoto(pid, id)

  return {'message': 'Photo uploaded successfully.', 'pid': pid}

def handle_mlwink(entry,values,files):
  id       = entry[COL_ID]
  location = entry[COL_LOCATION]
  country  = GazCountry(location)
  x        = entry[COL_X]
  y        = entry[COL_Y]
  tz       = entry[COL_TZ]

  id_to = int(values['id'])

  if Blocked(id_to, id):
    return {'error': 'This member has blocked you.'}

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  db.execute('SELECT email FROM profiles WHERE verified AND id=%d LIMIT 1' % (id_to))
  entry = db.fetchone()
  if not entry:
    return {'error': 'This member cannot be found.'}

  email   = entry[0]
  message = 'Wink!'

  now = datetime.datetime.utcnow()
  db.execute('INSERT INTO emails (id_from,id_to,message,sent) VALUES (%d,%d,%s,%s)' % (id, id_to, Quote(message), Quote(str(now))))
  db.commit()

  EmailWink(email, id, x, y, tz, unit_distance)

  return {'message': 'Your Wink! has been sent.'}
