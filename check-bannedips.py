import database

from utils import *
from mlutils import *

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT last_ip FROM profiles WHERE verified')
ips = set([(entry[0]) for entry in db.fetchall()])

with open('bannedips.txt','r') as file:
  for line in file.readlines():
    ip = line.strip()
    if ip in ips:
      print 'Banned ip address %s is registered' % (ip)
      db.execute('SELECT id,name,location,last_ip_country FROM profiles WHERE last_ip=%s' % (Quote(ip)))
      for entry in db.fetchall():
        print ' ', entry
