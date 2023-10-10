import os

from database import IPADDRESS_DB_URI, db_init
from model import RangeModel

BASE_DIR = os.path.dirname(__file__)

session = db_init(IPADDRESS_DB_URI)


def IpCountry(ip):
    def IpNumber(ip):
        s = ip.split(".")
        if len(s) < 4:
            raise Exception("Invalid IP address")
        return (int(s[0]) << 24) + (int(s[1]) << 16) + (int(s[2]) << 8) + int(s[3])

    if not ip:
        return "Unknown"

    n = IpNumber(ip)
    entry = session.query(RangeModel.country).filter(RangeModel.lower <= n, n <= RangeModel.upper).first()
    if not entry:
        return "Unknown"
    return entry.country
