#!/usr/bin/python

from mlhtml import *
from mlutils import *
from mllist import *
from mlemail import *

def EmailVerify(email,id):
  dict = {}
  dict['id'] = id
  dict['email'] = email

  html = RenderY('email-verify.html', dict)
  Email(email, 'Verify Registration', html, 1)

def EmailPassword(email,password):
  dict = {}
  dict['password'] = password

  html = RenderY('email-password.html', dict)
  Email(email, 'Password Reminder', html, 1)

def EmailKicked(email):
  dict = {}

  html = RenderY('email-kicked.html', dict)
  Email(email, 'Removal Alert', html)

def EmailKickedStopForumSpam(email):
  dict = {}

  html = RenderY('email-kicked-stopforumspam.html', dict)
  Email(email, 'Removal Alert', html)

def EmailPhotoDeleted(email):
  dict = {}

  html = RenderY('email-photo-deleted.html', dict)
  Email(email, 'Photo Removal Alert', html)

def EmailWink(email,id,x,y,tz,unit_distance):
  db = database.Database(MISS_LOOPY_DB)
  dict = {}
  dict['action']     = 'emailthread'
  dict['navigation'] = 'inbox'
  db.execute('SELECT * FROM profiles WHERE id=%d LIMIT 1' % (id))
  entry = db.fetchone()
  if not entry:
    return
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
  member['location']      = entry[COL_LOCATION]
  member['summary']       = mask.MaskEverything(entry[COL_SUMMARY])
  member['last_login']    = Since(entry[COL_LAST_LOGIN])
  member['login_country'] = entry[COL_LAST_IP_COUNTRY]
  member['created']       = Datetime(entry[COL_CREATED2], tz).strftime('%x')
  member['distance']      = Distance(distance, unit_distance)
  member['active']        = False
  dict['entry'] = member

  html = RenderY('email-wink.html', dict)
  Email(email, 'New Wink! Received', html)

def EmailNotify(email,id,x,y,tz,unit_distance):
  db = database.Database(MISS_LOOPY_DB)
  dict = {}
  dict['action']     = 'emailthread'
  dict['navigation'] = 'inbox'
  db.execute('SELECT * FROM profiles WHERE id=%d LIMIT 1' % (id))
  entry = db.fetchone()
  if not entry:
    return
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
  member['location']      = entry[COL_LOCATION]
  member['summary']       = mask.MaskEverything(entry[COL_SUMMARY])
  member['last_login']    = Since(entry[COL_LAST_LOGIN])
  member['login_country'] = entry[COL_LAST_IP_COUNTRY]
  member['created']       = Datetime(entry[COL_CREATED2], tz).strftime('%x')
  member['distance']      = Distance(distance, unit_distance)
  member['active']        = False
  dict['entry'] = member

  html = RenderY('email-notify.html', dict)
  Email(email, 'New Message Received', html)

def EmailNewMembers(email,ids,location,x,y,tz,unit_distance):
  db = database.Database(MISS_LOOPY_DB)
  dict = {}
  dict['action']     = 'member'
  dict['navigation'] = 'matches'
  dict['entries'] = ListMembers(ids,None,location,x,y,tz,unit_distance)

  html = RenderY('email-newmembers.html', dict)
  Email(email, 'New Members Available', html, 4)

def EmailInboxReminder(email,name):
  dict = {}
  dict['name'] = name

  html = RenderY('email-inbox-reminder.html', dict)
  Email(email, 'Unread Messages Reminder', html, 1)
