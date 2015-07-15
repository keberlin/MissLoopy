#!/usr/bin/python

import database

from utils import *
from mlutils import *
from emails import *

from logger import *

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT last_ip FROM profiles WHERE verified')
ips = set([(entry[0]) for entry in db.fetchall()])

ids = []
with open('bannedips.txt','r') as file:
  for line in file.readlines():
    ip = line.strip()
    if ip in ips:
      db.execute('SELECT id, email FROM profiles WHERE last_ip=%s' % (Quote(ip)))
      for entry in db.fetchall():
        ids.append((entry[0], entry[1]))

for id, email in ids:
  DeleteMember(id)
  EmailKickedStopForumSpam(email)
  logger.info('Kicked %d %s' % (id, email))
