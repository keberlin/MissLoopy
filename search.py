from datetime import date, datetime
import math
import os
import re

from sqlalchemy.sql.expression import or_

from gazetteer import *
from logger import logger
from mlutils import *
from model import *
from tzone import *
from utils import *


def search2(
    session,
    distance,
    sort,
    id,
    x,
    y,
    tz,
    gender,
    age,
    ethnicity,
    height,
    weight,
    gender_choice,
    age_min,
    age_max,
    ethnicity_choice,
    height_min,
    height_max,
    weight_choice,
):
    adjust = GazLatAdjust(y)

    query = session.query(ProfileModel).filter(ProfileModel.verified.is_(True))

    # Remove any mutually blocked profiles
    blocked_by_me = aliased(BlockedModel)
    blocked_by_them = aliased(BlockedModel)
    query = (
        query.outerjoin(blocked_by_me, and_(blocked_by_me.id == id, blocked_by_me.id_block == ProfileModel.id))
        .outerjoin(blocked_by_them, and_(blocked_by_them.id == ProfileModel.id, blocked_by_them.id_block == id))
        .filter(blocked_by_me.id.is_(None))
        .filter(blocked_by_them.id.is_(None))
    )

    # Limit profiles to those with genuine locations!
    # rules.append('last_ip_country = country')
    # Only list profiles which match this person's selection criteria
    if distance:
        dx = distance * 1000 / adjust  # Distance is stored in the db as metres so *1000
        dy = distance * 1000
        query = query.filter(x - dx <= ProfileModel.x, ProfileModel.x <= x + dx)
        query = query.filter(y - dy <= ProfileModel.y, ProfileModel.y <= y + dy)
    if gender_choice:
        query = query.filter(ProfileModel.gender.op("&")(gender_choice) != 0)
    if age_min:
        now = datetime.utcnow()
        ref = Datetime(now, tz)
        try:
            dob = date(ref.year - age_min, ref.month, ref.day)
        except ValueError:
            # cater for leap year
            dob = date(ref.year - age_min, ref.month, ref.day - 1)
        query = query.filter(ProfileModel.dob <= dob)
    if age_max:
        now = datetime.utcnow()
        ref = Datetime(now, tz)
        try:
            dob = date(ref.year - age_max - 1, ref.month, ref.day)
        except ValueError:
            # cater for leap year
            dob = date(ref.year - age_max - 1, ref.month, ref.day - 1)
        query = query.filter(ProfileModel.dob > dob)
    if ethnicity_choice:
        query = query.filter(ProfileModel.ethnicity.op("&")(ethnicity_choice) != 0)
    if height_min:
        query = query.filter(or_(ProfileModel.height.is_(None), ProfileModel.height >= height_min))
    if height_max:
        query = query.filter(or_(ProfileModel.height.is_(None), ProfileModel.height <= height_max))
    if weight_choice:
        query = query.filter(or_(ProfileModel.weight.is_(None), ProfileModel.weight.op("&")(weight_choice) != 0))

    # Only list profiles which match the other member's selection criteria
    query = query.filter(or_(ProfileModel.gender_choice.is_(None), ProfileModel.gender_choice.op("&")(gender) != 0))
    query = query.filter(or_(ProfileModel.age_min.is_(None), ProfileModel.age_min <= age))
    query = query.filter(or_(ProfileModel.age_max.is_(None), ProfileModel.age_max >= age))
    if ethnicity:
        query = query.filter(
            or_(ProfileModel.ethnicity_choice.is_(None), ProfileModel.ethnicity_choice.op("&")(ethnicity) != 0)
        )
    if height:
        query = query.filter(or_(ProfileModel.height_min.is_(None), ProfileModel.height_min <= height))
        query = query.filter(or_(ProfileModel.height_max.is_(None), ProfileModel.height_max >= height))
    if weight:
        query = query.filter(or_(ProfileModel.weight_choice.is_(None), ProfileModel.weight_choice.op("&")(weight) != 0))
    if sort:
        if sort == "age":
            query = query.order_by(ProfileModel.dob.desc())
        elif sort == "login":
            query = query.order_by(ProfileModel.last_login.desc())
        elif sort == "created":
            query = query.order_by(ProfileModel.created.desc())
        else:
            pass  # Order must be by distance

    entries = query.all()

    list = []
    for entry in entries:
        dx = abs(x - entry.x) * adjust / 1000
        dy = abs(y - entry.y) / 1000
        d = math.sqrt((dx * dx) + (dy * dy))
        if distance and d > distance:
            continue
        list.append((entry, d))
    if sort == "distance":
        list.sort(key=lambda a: a[1])  # TODO Move into the query itself

    return [x[0] for x in list]
