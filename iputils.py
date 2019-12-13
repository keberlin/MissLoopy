import os

import database

BASE_DIR = os.path.dirname(__file__)

IP_ADDRESS_DB = 'ipaddress'

def IpCountry(ip):
  def IpNumber(ip):
    s = ip.split('.')
    if len(s) < 4:
      raise Exception('Invalid IP address')
    return (int(s[0])<<24)+(int(s[1])<<16)+(int(s[2])<<8)+int(s[3])

  if not ip:
    return 'Unknown'

  db = database.Database(IP_ADDRESS_DB)

  n = IpNumber(ip)
  db.execute('SELECT country FROM ranges WHERE lower<=%d AND %d<=upper LIMIT 1' % (n, n))
  entry = db.fetchone()
  db.commit()
  if not entry:
    return 'Unknown'
  return entry[0]
