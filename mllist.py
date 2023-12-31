import itertools
import math

from database import db
from gazetteer import *
from logger import logger
import mask
from mlutils import *
from model import *
from tzone import *
from units import *
from utils import *


def ListMember(session, entry, active, location, x, y, tz, unit_distance):
    adjust = GazLatAdjust(y)
    dx = abs(x - entry.x) * adjust / 1000
    dy = abs(y - entry.y) / 1000
    distance = math.sqrt((dx * dx) + (dy * dy))

    member = {}
    member["id"] = entry.id
    member["image"] = PhotoFilename(MasterPhoto(session, entry.id))
    member["name"] = mask.MaskEverything(entry.name)
    member["gender"] = Gender(entry.gender)
    member["age"] = Age(entry.dob)
    member["starsign"] = Starsign(entry.dob)
    member["ethnicity"] = Ethnicity(entry.ethnicity)
    member["location"] = GazPlacename(entry.location, location)
    member["country"] = GazCountry(entry.location)
    member["summary"] = mask.MaskEverything(entry.summary)
    member["last_login"] = Since(entry.last_login)
    member["login_country"] = entry.last_ip_country
    member["created"] = Datetime(entry.created, tz).strftime("%x")
    member["distance"] = Distance(distance, unit_distance)
    member["active"] = active

    return member


def ListMembers(session, entries, counts, location, x, y, tz, unit_distance):
    members = []
    for entry, count in itertools.zip_longest(entries, counts if counts else []):
        member = ListMember(session, entry, count, location, x, y, tz, unit_distance)
        members.append(member)
    return members
