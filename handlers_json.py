import os, re, datetime, io, cStringIO, base64, psycopg2, time, logging

from PIL import Image

import search, spam, mask

from utils import *
from units import *
from localization import *
from gazetteer import *
from emails import *
from mlutils import *
from mlparse import *
from mlemail import *

from database import db
from model import *

BASE_DIR = os.path.dirname(__file__)

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

  id = entry.id

  # TODO Find a mechanism for updating a member's email address too..
  attributes = ['password']

  attrs = {}
  for attr in values:
    if not attr in attributes:
      continue
    if not values.get(attr):
      continue
    if attr.endswith('_choice'):
      attrs[attr] = eval(values[attr])
    else:
      attrs[attr] = values[attr][:MAX_LENGTH]
  for attr in attributes:
    if attr in attrs:
      continue
    attrs[attr] = None

  db.session.query(ProfilesModel).filter(ProfilesModel.id==id).update(attrs) 
  db.session.commit()

  return {'message': 'Account updated successfully.'}

def handle_mladdfavorite(entry,values,files):
  id = entry.id

  ids = map(lambda x:int(x), values['id'].split('|'))

  for id_favorite in ids:
    db.session.add(FavoritesModel(id=id, id_favorite=id_favorite))
  db.session.commit()

  if len(ids) == 1:
    return {'message': 'This member has been added to your favorites list.'}
  else:
    return {'message': 'These members have been added to your favorites list.'}

def handle_mlblock(entry,values,files):
  id = entry.id

  ids = map(lambda x:int(x), values['id'].split('|'))

  for id_block in ids:
    db.session.add(BlockedModel(id=id, id_block=id_block))
  db.session.commit()

  if len(ids) == 1:
    return {'message': 'This member has now been blocked.'}
  else:
    return {'message': 'These members have now been blocked.'}

def handle_mldeletefavorite(entry,values,files):
  id = entry.id

  if 'ids' in values: ids = values['ids']
  else: ids = map(lambda x:int(x), values['id'].split('|'))

  for id_favorite in ids:
    db.session.query(FavoritesModel).filter(FavoritesModel.id==id,FavoritesModel.id_favorite==id_favorite).delete() 
  db.session.commit()

  if len(ids) == 1:
    return {'message': 'This member has been removed from your favorites list.'}
  else:
    return {'message': 'These members have been removed from your favorites list.'}

def handle_mldeletephoto(entry,values,files):
  id = entry.id

  if 'pids' in values: pids = values['pids']
  else: pids = map(lambda x:int(x), values['pid'].split('|'))

  for pid in pids:
    # Ensure this member owns the photo first
    entry = db.session.query(PhotosModel.id).filter(PhotosModel.pid==pid).one_or_none() 
    if not entry:
      return {'error': 'Photo %d not found.' % (pid)}
    if entry.id != id:
      return {'error': 'You are not the owner of photo %d.' % (pid)}

  DeletePhotos(pids)

  deleted = pids

  pids = []
  master = 0
  entries = db.session.query(PhotosModel.pid,PhotosModel.master).filter(PhotosModel.id==id).all() 
  for entry in entries:
    pids.append(entry.pid)
    if entry.master:
      master = entry.pid

  if len(deleted) == 1:
    return {'message': 'This photo has been deleted.', 'pids': pids, 'master': master}
  else:
    return {'message': 'These photos have been deleted.', 'pids': pids, 'master': master}

def handle_mlmasterphoto(entry,values,files):
  if not values.get('pid'):
    return {'error': 'No Photo selected.'}

  id = entry.id

  pid = int(values['pid'])

  # Ensure this member owns the photo first
  entry = db.session.query(PhotosModel.id).filter(PhotosModel.pid==pid).one_or_none() 
  if entry.id != id:
    return {'error': 'You are not the owner of this photo.'}
  # Remove the master flag from all photos
  db.session.query(PhotosModel).filter(PhotosModel.id==id).update({"master":False}) 
  # Restore the master flag for the selected photo
  db.session.query(PhotosModel).filter(PhotosModel.pid==pid).update({"master":True}) 
  db.session.commit()

  pids = []
  master = 0
  entries = db.session.query(PhotosModel.pid,PhotosModel.master).filter(PhotosModel.id==id).all() 
  for entry in entries:
    pids.append(entry.pid)
    if entry.master:
      master = entry.pid

  return {'message': 'This photo has been set to your main profile photo.', 'pids': pids, 'master': master}

def handle_mlprofile(entry,values,files):
  if not values.get('name'):
    return {'error': 'No Display Name specified.'}

  id = entry.id

  ParseHeight(values, 'height')

  attributes = ['name', 'gender', 'ethnicity', 'height', 'weight', 'education', 'status', 'smoking', 'drinking', 'occupation', 'summary', 'description']

  attrs = {}
  if 'location' in values:
    tuple = GazLocation(values['location'])
    if not tuple:
      return {'matches': GazClosestMatches(values['location'], MAX_MATCHES)}
    attrs['location'] = values['location']
    attrs['country'] = GazCountry(values['location'])
    attrs['x'] = tuple[0]
    attrs['y'] = tuple[1]
    attrs['tz'] = tuple[2]
  for attr in values:
    if not attr in attributes:
      continue
    if not values.get(attr):
      continue
    if attr.endswith('_choice'):
      attrs[attr] = eval(values[attr])
    else:
      attrs[attr] = values[attr][:MAX_LENGTH].encode('utf-8')
  for attr in attributes:
    if attr in attrs:
      continue
    attrs[attr] = None

  db.session.query(ProfilesModel).filter(ProfilesModel.id==id).update(attrs) 
  db.session.commit()

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

  email    = values['email'].lower()
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

  entry = db.session.query(ProfilesModel).filter(ProfilesModel.email==email).one_or_none() 
  if entry:
    return {'error': 'Email Address already in use.'}

  attributes = ['email', 'password', 'name', 'gender', 'ethnicity',
                'height', 'weight', 'education', 'status', 'smoking', 'drinking', 'occupation', 'summary', 'description',
                'gender_choice', 'ethnicity_choice', 'age_min', 'age_max', 'height_min', 'height_max', 'weight_choice', 'looking_for']

  attrs = {}
  now = datetime.datetime.utcnow()
  attrs['created2'] = now
  attrs['dob'] = dt.strftime('%Y-%m-%d')
  if 'location' in values:
    tuple = GazLocation(values['location'])
    if not tuple:
      return {'matches': GazClosestMatches(values['location'], MAX_MATCHES)}
    attrs['location'] = values['location']
    attrs['country'] = GazCountry(values['location'])
    attrs['x'] = tuple[0]
    attrs['y'] = tuple[1]
    attrs['tz'] = tuple[2]
  for attr in values:
    if not attr in attributes:
      continue
    if not values.get(attr):
      continue
    if attr.endswith('_choice'):
      attrs[attr] = eval(values[attr])
    else:
      attrs[attr] = values[attr][:MAX_LENGTH]
  for attr in attributes:
    if attr in attrs:
      continue
    attrs[attr] = None

  db.session.add(ProfilesModel(attrs))
  db.session.commit()

  EmailVerify(email,id)

  return {'code': 1002}

def handle_mlpassword(entry,values,files):
  if not values.get('email'):
    return {'error': 'No email specified.'}

  email = values['email'].lower()

  # Retrieve the password
  entry = db.session.query(ProfilesModel.password).filter(ProfilesModel.email==email).one_or_none() 
  if not entry:
    return {'error': 'Email Address not found.'}

  EmailPassword(email,entry.password)

  return {'message': 'Your password reminder has been sent...'}

def handle_mlresend(entry,values,files):
  if not values.get('email'):
    return {'error': 'No email specified.'}

  email = values['email'].lower()

  # Retrieve the newly created id
  entry = db.session.query(ProfilesModel.id).filter(ProfilesModel.email==email).one_or_none() 
  if not entry:
    return {'error': 'Account not found.'}

  EmailVerify(email,entry.id)

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
  id = entry.id

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
      attrs[attr] = eval(values[attr])
    else:
      attrs[attr] = values[attr][:MAX_LENGTH]
  for attr in attributes:
    if attr in attrs:
      continue
    attrs[attr] = None

  db.session.query(ProfilesModel).filter(ProfilesModel.id==id).update(attrs) 
  db.session.commit()

  return {'message': 'Seeking updated successfully.'}

def handle_mlsendemail(entry,values,files):
  id       = entry.id
  location = entry.location
  country  = GazCountry(location)
  x        = entry.x
  y        = entry.y
  tz       = entry.tz

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
  if spam.IsSpamFactored(tuple, spammer, 3):
    with open(os.path.join(BASE_DIR, 'junk-auto.log'), 'a') as f:
      f.write('%d %s\n' % (id, re.sub('[\r\n]+',' ',message).encode('utf-8')))

  entry_to = db.session.query(ProfilesModel).filter(ProfilesModel.id==id_to).one_or_none() 
  if not entry_to:
    return {'error': 'This member cannot be found.'}

  notifications = entry_to.notifications

  now = datetime.datetime.utcnow()
  db.session.add(EmailsModel(id_from=id, id_to=id_to, message=message, sent=now))
  db.session.commit()

  if not notifications & NOT_NEW_MESSAGE:
    EmailNotify(entry_to, entry)

  d = {}
  d['sent']     = True
  d['message']  = message
  d['image']    = None
  d['time']     = Since(now, False)
  d['viewed']   = False

  return {'message': 'Your message has been sent.', 'entry': d}

def handle_mlsendphoto(entry,values,files):
  IMAGE_MAX_SIZE = 400

  id       = entry.id
  location = entry.location
  country  = GazCountry(location)
  x        = entry.x
  y        = entry.y
  tz       = entry.tz

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
  image = 'data:image/jpg;base64,' + base64.b64encode(data.getvalue())

  entry_to = db.session.query(ProfilesModel).filter(ProfilesModel.id==id_to).one_or_none() 
  if not entry_to:
    return {'error': 'This member cannot be found.'}

  notifications = entry_to.notifications

  now = datetime.datetime.utcnow()
  db.session.add(EmailsModel(id_from=id, id_to=id_to, image=image, sent=now))
  db.session.commit()

  if not notifications & NOT_NEW_MESSAGE:
    EmailNotify(entry_to, entry)

  d = {}
  d['sent']     = True
  d['message']  = None
  d['image']    = image
  d['time']     = Since(now, False)
  d['viewed']   = False

  return {'message': 'Your photo has been sent.', 'entry': d}

def handle_mlspam(entry,values,files):
  id = entry.id

  id_spam = int(values['id'])

  with open(os.path.join(BASE_DIR, 'junk-reported.log'), 'a') as f:
    entries = db.session.query(EmailsModel.message).filter(EmailsModel.id_from==id_spam, EmailsModel.id_to==id).distinct().all() 
    for entry in entries:
      f.write('%d %s\n' % (id_spam, re.sub('[\r\n]+',' ',entry.message).encode('utf-8')))
    db.session.commit()

  return {'message': 'Thank you for reporting this member...'}

def handle_mlunblock(entry,values,files):
  id = entry.id

  if 'ids' in values: ids = values['ids']
  else: ids = map(lambda x:int(x), values['id'].split('|'))

  for id_block in ids:
    db.session.query(BlockedModel).filter(BlockedModel.id==id, BlockedModel.id_block==id_block).delete()
  db.session.commit()

  if len(ids) == 1:
    return {'message': 'This member has now been unblocked.'}
  else:
    return {'message': 'These members have now been unblocked.'}

def handle_mluploadphoto(entry,values,files):
  IMAGE_MIN_SIZE = 100
  IMAGE_MAX_SIZE = 600

  id = entry.id

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

  now = datetime.datetime.utcnow()
  entry = db.session.add(PhotosModel(id=id, created=now))
  db.session.commit()

  # Create a photo file using pid and copy data into it
  filename = os.path.join(BASE_DIR, 'static', PhotoFilename(entry.pid))
  if os.path.isfile(filename):
    logging.error('ERROR: Photo file %s already exists!' % (filename))
    os.remove(filename)

  # Save the modified photo
  im = im.convert('RGB')
  im.save(filename, 'JPEG')

  EmailNewPhoto(filename, pid, id)

  pids = []
  master = 0
  entries = db.session.query(PhotosModel.pid, PhotosModel.master).filter(PhotosModel.id==id).all()
  for entry in entries:
    pids.append(entry.pid)
    if entry.master:
      master = entry.pid

  return {'message': 'Photo uploaded successfully.', 'pids': pids, 'master': master}

def handle_mlwink(entry,values,files):
  id       = entry.id
  location = entry.location
  country  = GazCountry(location)
  x        = entry.x
  y        = entry.y
  tz       = entry.tz

  id_to = int(values['id'])

  if Blocked(id_to, id):
    return {'error': 'This member has blocked you.'}

  SetLocale(country)

  unit_distance, unit_height = Units(country)

  entry_to = db.session.query(ProfilesModel).filter(ProfilesModel.id==id_to, ProfilesModel.verified.is_(True)).one_or_none()
  if not entry_to:
    return {'error': 'This member cannot be found.'}

  notifications = entry_to.notifications

  message = 'Wink!'

  now = datetime.datetime.utcnow()
  db.session.add(EmailsModel(id_from=id, id_to=id_to, message=message, sent=now))
  db.session.commit()

  if not notifications & NOT_NEW_MESSAGE:
    EmailWink(entry_to, entry)

  return {'message': 'Your Wink! has been sent.'}
