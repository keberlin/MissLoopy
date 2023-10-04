import os

from database import IPADDRESS_DB_URI, db_init

BASE_DIR = os.path.dirname(__file__)

session = db_init(IPADDRESS_DB_URI)

def IpCountry(ip):
  def IpNumber(ip):
    s = ip.split('.')
    if len(s) < 4:
      raise Exception('Invalid IP address')
    return (int(s[0])<<24)+(int(s[1])<<16)+(int(s[2])<<8)+int(s[3])

  if not ip:
    return 'Unknown'

  n = IpNumber(ip)
  entry = session.query(RangeModel.country).filter(lower<=n,n<=upper).first()
  if not entry:
    return 'Unknown'
  return entry.country
