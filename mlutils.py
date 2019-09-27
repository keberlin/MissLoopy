import os, datetime, cStringIO, base64

import database

import logger

from PIL import Image

from utils import *
from iputils import *

BASE_DIR = os.path.dirname(__file__)

MISS_LOOPY_DB = 'missloopy'

AGE_MIN = 18
AGE_MAX = 99
HEIGHT_MIN = 120
HEIGHT_MAX = 250

# Columns in profiles
COL_ID               = 0
COL_EMAIL            = 1
COL_PASSWORD         = 2
COL_CREATED_OLD      = 3
COL_VERIFIED         = 4
COL_LAST_LOGIN       = 5
COL_NAME             = 6
COL_GENDER           = 7
COL_DOB              = 8
COL_HEIGHT           = 9
COL_WEIGHT           = 10
COL_ETHNICITY        = 11
COL_EDUCATION        = 12
COL_STATUS           = 13
COL_SMOKING          = 14
COL_DRINKING         = 15
COL_COUNTRY          = 16
COL_REGION_OLD       = 17
COL_PLACENAME_OLD    = 18
COL_X                = 19
COL_Y                = 20
COL_TZ               = 21
COL_OCCUPATION       = 22
COL_SUMMARY          = 23
COL_DESCRIPTION      = 24
COL_LOOKING_FOR      = 25
COL_GENDER_CHOICE    = 26
COL_AGE_MIN          = 27
COL_AGE_MAX          = 28
COL_HEIGHT_MIN       = 29
COL_HEIGHT_MAX       = 30
COL_WEIGHT_CHOICE    = 31
COL_ETHNICITY_CHOICE = 32
COL_LOCATION         = 33
COL_LAST_IP          = 34
COL_CREATED2         = 35
COL_LAST_IP_COUNTRY  = 36
COL_NOTIFICATIONS    = 37

# Columns in photos
COL3_PID    = 0
COL3_ID     = 1
COL3_OFFSET = 2
COL3_MASTER = 3

# Columns in emails
COL4_ID_FROM = 0
COL4_ID_TO   = 1
COL4_MESSAGE = 2
COL4_SENT    = 3
COL4_VIEWED  = 4
COL4_IMAGE   = 5

# Columns in blocked
COL6_ID       = 0
COL6_ID_BLOCK = 1

# Columns in favorites
COL7_ID          = 0
COL7_ID_FAVORITE = 1

# Columns in results
COL5_ID          = 0
COL5_ID_SEARCH   = 1
COL5_ID_PREVIOUS = 2
COL5_ID_NEXT     = 3

# Gender enum
GEN_MAN        = 1<<0
GEN_WOMAN      = 1<<1
GEN_SUGAR_PUP   = 1<<2
GEN_SUGAR_BABY  = 1<<3
GEN_SUGAR_DADDY = 1<<4
GEN_SUGAR_MOMMA = 1<<5

# Ethnicity enum
ETH_WHITE  = 1<<0
ETH_BLACK  = 1<<1
ETH_LATINO = 1<<2
ETH_ASIAN  = 1<<3
ETH_MIXED  = 1<<4
ETH_OTHER  = 1<<5
ETH_INDIAN = 1<<6

# Weight enum
WGT_SLIM         = 1<<0
WGT_ATHLETIC     = 1<<1
WGT_AVERAGE      = 1<<2
WGT_EXTRA_POUNDS = 1<<3
WGT_LARGE        = 1<<4

# Education enum
EDU_SCHOOL     = 1<<0
EDU_HIGHER     = 1<<1
EDU_UNIVERSITY = 1<<2

# Status enum
STA_SINGLE       = 1<<0
STA_MARRIED      = 1<<1
STA_COHABITATING = 1<<2
STA_WITH_FRIENDS = 1<<3
STA_WITH_FAMILY  = 1<<4
STA_COMPLICATED  = 1<<5

# Smoking enum
SMO_NEVER   = 1<<0
SMO_SOCIAL  = 1<<1
SMO_REGULAR = 1<<2
SMO_HEAVY   = 1<<3

# Drinking enum
DRI_NEVER   = 1<<0
DRI_SOCIAL  = 1<<1
DRI_REGULAR = 1<<2
DRI_HEAVY   = 1<<3

# Notification enum
NOT_NEW_MEMBERS = 1<<0
NOT_NEW_MESSAGE = 1<<1

PHOTOS_DIR   = 'photos'
MEMBERS_DIR  = 'members'
SCAMMERS_DIR = 'scammers'

db = database.Database(MISS_LOOPY_DB)

def Range(min,max):
  if min and max:
    return 'from %s to %s' % (str(min), str(max))
  if min:
    return 'at least %s' % (str(min))
  if max:
    return 'no more than %s' % (str(max))
  return None

def Gender(enum):
  if not enum:
    return None
  if enum&GEN_MAN:
    return 'Man'
  if enum&GEN_WOMAN:
    return 'Woman'
  if enum&GEN_SUGAR_PUP:
    return 'Sugar Pup'
  if enum&GEN_SUGAR_BABY:
    return 'Sugar Baby'
  if enum&GEN_SUGAR_DADDY:
    return 'Sugar Daddy'
  if enum&GEN_SUGAR_MOMMA:
    return 'Sugar Momma'
  return None

def GenderList(enum):
  if not enum:
    return None
  list = []
  if enum&GEN_MAN:
    list.append('Men')
  if enum&GEN_WOMAN:
    list.append('Women')
  if enum&GEN_SUGAR_PUP:
    list.append('Sugar Pups')
  if enum&GEN_SUGAR_BABY:
    list.append('Sugar Babies')
  if enum&GEN_SUGAR_DADDY:
    list.append('Sugar Daddies')
  if enum&GEN_SUGAR_MOMMA:
    list.append('Sugar Mommas')
  return ' or '.join(list)

def Ethnicity(enum):
  if not enum:
    return None
  if enum&ETH_WHITE:
    return 'White'
  if enum&ETH_BLACK:
    return 'Black'
  if enum&ETH_LATINO:
    return 'Latino'
  if enum&ETH_ASIAN:
    return 'Asian'
  if enum&ETH_MIXED:
    return 'Mixed'
  if enum&ETH_OTHER:
    return 'Other'
  return None

def EthnicityList(enum):
  if not enum:
    return None
  list = []
  if enum&ETH_WHITE:
    list.append('White')
  if enum&ETH_BLACK:
    list.append('Black')
  if enum&ETH_LATINO:
    list.append('Latino')
  if enum&ETH_ASIAN:
    list.append('Asian')
  if enum&ETH_MIXED:
    list.append('Mixed')
  if enum&ETH_OTHER:
    list.append('Other')
  return ' or '.join(list)

def Weight(enum):
  if not enum:
    return None
  if enum&WGT_SLIM:
    return 'Slim'
  if enum&WGT_ATHLETIC:
    return 'Athletic'
  if enum&WGT_AVERAGE:
    return 'Average'
  if enum&WGT_EXTRA_POUNDS:
    return 'A few extra pounds'
  if enum&WGT_LARGE:
    return 'Large'
  return None

def Education(enum):
  if not enum:
    return None
  if enum&EDU_SCHOOL:
    return 'School'
  if enum&EDU_HIGHER:
    return 'College'
  if enum&EDU_UNIVERSITY:
    return 'University'
  return None

def Status(enum):
  if not enum:
    return None
  if enum&STA_SINGLE:
    return 'Single'
  if enum&STA_MARRIED:
    return 'Married'
  if enum&STA_COHABITATING:
    return 'Cohabitating'
  if enum&STA_WITH_FRIENDS:
    return 'With friends'
  if enum&STA_WITH_FAMILY:
    return 'With family'
  if enum&STA_COMPLICATED:
    return 'It\'s complicated'
  return None

def Smoking(enum):
  if not enum:
    return None
  if enum&SMO_NEVER:
    return 'Never'
  if enum&SMO_SOCIAL:
    return 'Social'
  if enum&SMO_REGULAR:
    return 'Regular'
  if enum&SMO_HEAVY:
    return 'Heavy'
  return None

def Drinking(enum):
  if not enum:
    return None
  if enum&DRI_NEVER:
    return 'Never'
  if enum&DRI_SOCIAL:
    return 'Social'
  if enum&DRI_REGULAR:
    return 'Regular'
  if enum&DRI_HEAVY:
    return 'Heavy'
  return None

def ImageData(filename):
  im = Image.open(filename)
  data = cStringIO.StringIO()
  im.save(data, 'JPEG')
  return 'data:image/jpg;base64,' + base64.b64encode(data.getvalue())

def ImageDimensions(filename):
  im = Image.open(filename)
  return im.size

def PhotoFilename(pid):
  if pid > 0:
    name = 'img%d' % (pid)
  else:
    name = 'dummy'
  return os.path.join(PHOTOS_DIR, name + '.jpg')

def MasterPhoto(id):
  db.execute('SELECT pid FROM photos WHERE id=%d AND master LIMIT 1' % (id))
  entry = db.fetchone()
  if not entry:
    db.execute('SELECT pid FROM photos WHERE id=%d LIMIT 1' % (id))
    entry = db.fetchone()
    if not entry:
      return 0
  return entry[0]

def Login(email,password):
  # Authenticate
  db.execute('SELECT * FROM profiles WHERE email ILIKE %s LIMIT 1' % (Quote(email)))
  entry = db.fetchone()
  if not entry:
    return {'error': 'Email Address not found.'}
  if entry[COL_PASSWORD] != password:
    return {'error': 'Password does not match.'}
  if not entry[COL_VERIFIED]:
    return {'code': 1001}

  id = entry[COL_ID]

  return {'id': id}

def Authenticate(cookies=None,remote_addr=None):
  if not cookies:
    cookies = FetchCookies()
  if not cookies:
    return None

  if 'id' not in cookies:
    return None
  if 'email' not in cookies:
    return None
  if 'password' not in cookies:
    return None

  id       = int(cookies['id'])
  email    = cookies['email']
  password = cookies['password']

  # Authenticate
  db.execute('SELECT * FROM profiles WHERE id=%d AND email ILIKE %s AND password=%s LIMIT 1' % (id, Quote(email), Quote(password)))
  entry = db.fetchone()
  if not entry:
    return None

  now = datetime.datetime.utcnow()
  db.execute('UPDATE profiles SET last_login=%s WHERE id=%d' % (Quote(str(now)), id))
  db.commit()
  if not remote_addr:
    remote_addr = FetchRemoteAddr()
  if remote_addr and entry[COL_LAST_IP] != remote_addr:
    db.execute('UPDATE profiles SET last_ip=%s,last_ip_country=%s WHERE id=%d' % (Quote(remote_addr), Quote(IpCountry(remote_addr)), id))
    db.commit()

  return entry

def Blocked(id,id_with):
  db.execute('SELECT COUNT(*) FROM blocked WHERE id=%d AND id_block=%d' % (id, id_with))
  entry = db.fetchone()
  return (entry[0] > 0)

def BlockedMutually(id,id_with):
  db.execute('SELECT COUNT(*) FROM blocked WHERE (id=%d AND id_block=%d) OR (id=%d AND id_block=%d)' % (id, id_with, id_with, id))
  entry = db.fetchone()
  return (entry[0] > 0)

def DeletePhoto(pid):
  # Remove photo file using pid
  db.execute('DELETE FROM photos WHERE pid=%d' % (pid))
  db.commit()
  filename = os.path.join(BASE_DIR, 'static', PhotoFilename(pid))
  try:
    os.remove(filename)
  except:
    logger.error('ERROR: os.remove(%s) failed!' % filename)

def DeletePhotos(pids):
  for pid in pids:
    DeletePhoto(pid)

def DeleteMember(id):
  db.execute('DELETE FROM profiles WHERE id=%d' % (id))
  db.execute('SELECT pid FROM photos WHERE id=%d' % (id))
  pids = [(entry[0]) for entry in db.fetchall()]
  DeletePhotos(pids)
  db.execute('DELETE FROM favorites WHERE id=%d OR id_favorite=%d' % (id, id))
  db.execute('DELETE FROM blocked WHERE id=%d OR id_block=%d' % (id, id))
  db.execute('DELETE FROM emails WHERE id_from=%d OR id_to=%d' % (id, id))
  db.execute('DELETE FROM results WHERE id=%d' % (id))
  #PurgeResults(id)
  db.commit()

def InboxCount(id):
  db.execute('SELECT COUNT(*) FROM emails WHERE id_to=%d AND not viewed AND id_from NOT IN (SELECT id_block FROM blocked WHERE id=id_to) AND id_to NOT IN (SELECT id_block FROM blocked WHERE id=id_from)' % (id))
  entry = db.fetchone()
  return entry[0]

def OutboxCount(id):
  db.execute('SELECT COUNT(*) FROM emails WHERE id_from=%d AND not viewed AND id_from NOT IN (SELECT id_block FROM blocked WHERE id=id_to) AND id_to NOT IN (SELECT id_block FROM blocked WHERE id=id_from)' % (id))
  entry = db.fetchone()
  return entry[0]

def SaveResults(id,results):
  db.execute('DELETE FROM results WHERE id=%d' % (id))
  for i in range(len(results)):
    id_previous = results[i-1] if i > 0 else 0
    id_search = results[i]
    id_next = results[i+1] if i < len(results)-1 else 0
    db.execute('INSERT INTO results (id, id_search, id_previous, id_next) VALUES (%d,%d,%d,%d)' % (id, id_search, id_previous, id_next))
  db.commit()

def PreviousResult(id,id_search):
  db.execute('SELECT id_previous FROM results WHERE id=%d AND id_search=%d LIMIT 1' % (id, id_search))
  entry = db.fetchone()
  if not entry:
    return 0
  return entry[0]

def NextResult(id,id_search):
  db.execute('SELECT id_next FROM results WHERE id=%d AND id_search=%d LIMIT 1' % (id, id_search))
  entry = db.fetchone()
  if not entry:
    return 0
  return entry[0]

def PurgeResults(id_search):
  db.execute('SELECT * FROM results WHERE id_search=%d' % (id_search))
  for entry in db.fetchall():
    id          = entry[COL5_ID]
    id_previous = entry[COL5_ID_PREVIOUS]
    id_next     = entry[COL5_ID_NEXT]
    if id_previous:
      db.execute('UPDATE results SET id_next=%d WHERE id=%d AND id_search=%d' % (id_next, id, id_previous))
    if id_next:
      db.execute('UPDATE results SET id_previous=%d WHERE id=%d AND id_search=%d' % (id_previous, id, id_next))
  db.commit()
