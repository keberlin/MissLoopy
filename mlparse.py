from datetime import datetime
import re

from logger import logger
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


def ParseAge(ss):
    if not ss:
        return
    ss = re.sub(r"[^0-9]", r" ", ss)
    v = ParseNumber(ss)
    if v is not None:
        return min(max(int(v), AGE_MIN), AGE_MAX)
    logger.error(f"ERROR: Did not understand age: {ss}")


def ParseHeight(ss):
    if not ss:
        return
    ss = ss.replace(r",", r".")
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
        return min(max(int(v), HEIGHT_MIN), HEIGHT_MAX)
    # Assume it's in feet & inches
    s = ss.split()
    if len(s) >= 2:
        v1 = ParseNumber(s[0])
        v2 = ParseNumber(s[1])
        if v1 is not None and v2 is not None:
            v = (v1 * 12 + v2) * 2.54
            return min(max(int(v), HEIGHT_MIN), HEIGHT_MAX)
    logger.error(f"ERROR: Did not understand height: {ss}")


def ParseRange(min, max):
    if not min is None and not max is None:
        if max < min:
            return max, min
    return min, max


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
            return datetime.strptime(s, f)
        except:
            pass
    return None


def ParseEmail(email):
    return re.search("^[\w\*\-\.#=%\?\$'!/{}~]+@[\w\-]+(\.[\w\-]+)+$", email)
