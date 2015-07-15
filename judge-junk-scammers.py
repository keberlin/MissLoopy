#!/usr/bin/python

import csv, requests

import database

from utils import *
from gazetteer import *
from mlutils import *
from emails import *

from logger import *

def StopForumSpamAdd(username,email,ip,evidence):
  data = {
    'username': username,
    'email': email,
    'ip': ip,
    'api_key': 'dejcsw8ph7iu5n',
    'evidence': evidence
  }
  requests.post('http://www.stopforumspam.com/add',data)

ids = set()
with open('junk-auto.log', 'r') as file:
  for line in file.readlines():
    line = line.decode('utf-8','ignore')
    words = line.split()
    ids.add(int(words[0]))
with open('junk-reported.log', 'r') as file:
  for line in file.readlines():
    line = line.decode('utf-8','ignore')
    words = line.split()
    try:
      ids.add(int(words[0]))
    except:
      pass

db = database.Database(MISS_LOOPY_DB)

ids = list(ids)
ids.sort()
ids.reverse()
for id in ids:
  db.execute('SELECT * FROM profiles WHERE id=%d LIMIT 1' % (id))
  entry = db.fetchone()
  if not entry:
    continue
  ip = entry[COL_LAST_IP]
  email = entry[COL_EMAIL]
  name = entry[COL_NAME]
  country = GazCountry(entry[COL_LOCATION])
  last_login_country = entry[COL_LAST_IP_COUNTRY]
  db.execute('SELECT message FROM emails WHERE id_from=%d AND message NOT LIKE "data:image/%%" ORDER BY LENGTH(message) DESC LIMIT 1' % (id))
  entry = db.fetchone()
  if not entry:
    continue
  message = entry[0]
  db.execute('SELECT COUNT(DISTINCT id_to) FROM emails WHERE id_from=%d' % (id))
  entry = db.fetchone()
  members = entry[0]
  out = '%d: %d, %s, %s, "%s", %s, (%s), "%s"' % (id, members, ip, email, name, country, last_login_country, message)
  print
  print
  print out.encode('utf-8')
  print
  kick = raw_input('Kick? ')
  if kick=='y':
    StopForumSpamAdd(name,email,ip,message)
    DeleteMember(id)
    EmailKickedStopForumSpam(email)
    logger.info('Kicked %d %s' % (id, email))
  elif kick=='q':
    break
