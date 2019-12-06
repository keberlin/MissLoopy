import csv, requests

import database

from utils import *
from gazetteer import *
from mlutils import *
from emails import *

from logger import *

ids = set()
with open('junk-auto.log', 'r') as file:
  for line in file.readlines():
    line = line.decode('utf-8','ignore')
    words = line.split()
    ids.add(words[0])
with open('junk-reported.log', 'r') as file:
  for line in file.readlines():
    line = line.decode('utf-8','ignore')
    words = line.split()
    ids.add(words[0])

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT id_from,MAX(sent) FROM emails WHERE id_from IN (%s) GROUP BY id_from ORDER BY MAX(sent) DESC' % (','.join(list(ids))))
ids = [x[0] for x in db.fetchall()]

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
  db.execute("SELECT message, sent FROM emails WHERE id_from=%d ORDER BY LENGTH(message) DESC LIMIT 1" % (id))
  entry = db.fetchone()
  if not entry:
    continue
  message = entry[0]
  db.execute('SELECT COUNT(DISTINCT id_to) FROM emails WHERE id_from=%d' % (id))
  entry = db.fetchone()
  members = entry[0]
  out = '%d: %d, %s, %s, "%s", %s, (%s), "%s"' % (id, members, ip, email, name, country, last_login_country, message)
  db.execute('SELECT DISTINCT id_to FROM emails WHERE id_from=%d' % (id))
  entry = db.fetchall()
  id_tos = [v[0] for v in entry]
  tos = []
  for id_to in id_tos[:10]:
    db.execute('SELECT * FROM profiles WHERE id=%d LIMIT 1' % (id_to))
    entry = db.fetchone()
    to = '%d: "%s", %s' % (id_to, entry[COL_NAME], GazCountry(entry[COL_LOCATION]))
    tos.append(to)
  print
  print
  print out.encode('utf-8')
  for to in tos:
    print '  ', to.encode('utf-8')
  print
  kick = raw_input('Kick? ')
  if kick=='y':
    StopForumSpamAdd(name,email,ip,message)
    DeleteMember(id)
    EmailKicked(email)
    logger.info('Kicked due to spamming %s %d %s' % (Quote(ip), id, email))
  elif kick=='q':
    break
