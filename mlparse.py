import logging
import re

from mlutils import *

# Need these to counter the fact that IE does not support HTML5 properly!


def ParseNumber(ss):
    # See if it's an integer
    try:
        return int(ss)
    except:
        # See if it's a float
        try:
            return float(ss)
        except:
            pass
    return None


def ParseAge(dict, key):
    if not dict.get(key):
        return
    ss = re.sub(r"[^0-9]", r" ", dict[key])
    v = ParseNumber(ss)
    if v is not None:
        dict[key] = str(min(max(int(v), AGE_MIN), AGE_MAX))
        return
    logging.error("ERROR: Did not understand age: %s" % (dict[key]))
    del dict[key]


def ParseHeight(dict, key):
    if not dict.get(key):
        return
    ss = dict[key].replace(r",", r".")
    ss = re.sub(r"[^0-9\.]", r" ", ss)
    ss = re.sub(r" *\. *", r".", ss)
    v = ParseNumber(ss)
    if v is not None:
        # See if it's in metres
        if v < 3:
            v = v * 100
        # See if it's in feet
        elif v < 10:
            v = v * 12 * 2.54
        else:
            # Assume it's in centimetres
            pass
        dict[key] = str(min(max(int(v), HEIGHT_MIN), HEIGHT_MAX))
        return
    # Assume it's in feet & inches
    s = ss.split()
    if len(s) >= 2:
        v1 = ParseNumber(s[0])
        v2 = ParseNumber(s[1])
        if v1 is not None and v2 is not None:
            v = (v1 * 12 + v2) * 2.54
            dict[key] = str(min(max(int(v), HEIGHT_MIN), HEIGHT_MAX))
            return
    logging.error("ERROR: Did not understand height: %s" % (dict[key]))
    del dict[key]


def ParseRange(dict, kmin, kmax):
    if not dict.get(kmin) or not dict.get(kmax):
        return
    vmin = int(dict[kmin])
    vmax = int(dict[kmax])
    if vmax < vmin:
        dict[kmin] = str(vmax)
        dict[kmax] = str(vmin)


def ParseDob(dob):
    s = re.sub("[\W_]+", " ", dob).strip()
    formats = [
        "%Y %m %d",
        "%Y%m%d",
        "%Y %d %m",
        "%Y%d%m",
        "%m %d %Y",
        "%m%d%Y",
        "%d %m %Y",
        "%d%m%Y",
        "%d %B %Y",
        "%d %b %Y",
        "%d%B %Y",
        "%d%b %Y",
        "%B %d %Y",
        "%b %d %Y",
        "%B%d %Y",
        "%b%d %Y",
        "%Y %B %d",
        "%Y %b %d",
        "%Y%B %d",
        "%Y%b %d",
        "%Y %B%d",
        "%Y %b%d",
        "%Y%B%d",
        "%Y%b%d",
        "%Y %d %B",
        "%Y %d %b",
        "%Y %d%B",
        "%Y %d%b",
    ]
    for f in formats:
        try:
            return datetime.datetime.strptime(s, f)
        except:
            pass
    return None


def ParseEmail(email):
    return re.search("^[\w\*\-\.#=%\?\$'!/{}~]+@[\w\-]+(\.[\w\-]+)+$", email)
