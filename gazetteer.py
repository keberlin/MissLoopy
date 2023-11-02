import difflib
import math
import os
import re

from sqlalchemy.sql import func

from database import db_init, GAZETTEER_DB_URI
from model import LocationModel
from utils import *

session = db_init(GAZETTEER_DB_URI)

CIRCUM_X = 40075017
CIRCUM_Y = 40007860


def GazLatAdjust(y):
    return math.cos(y * 2 * math.pi / CIRCUM_Y)


def GazLocation(location):
    entry = (
        session.query(LocationModel.x, LocationModel.y, LocationModel.tz)
        .filter(LocationModel.location == location)
        .one_or_none()
    )
    return entry


def Alias(query):
    str = re.sub(r"\W", r"", query).lower()
    if str == "us" or str == "usa" or str == "america":
        return "United States"
    if str == "uk" or str == "britain":
        return "United Kingdom"
    if str == "uae":
        return "United Arab Emirates"
    if str == "rwp":
        return "Rawalpindi"
    return None


def GazClosestMatchesQuick(query, max):
    alias = Alias(query)
    if alias:
        query = alias

    closest = []

    entries = (
        session.query(LocationModel.location)
        .filter(LocationModel.location.ilike(query))
        .order_by(LocationModel.population.desc())
        .limit(max)
        .all()
    )
    closest.extend([(entry.location) for entry in entries])
    if len(closest) < max:
        entries = (
            session.query(LocationModel.location)
            .filter(LocationModel.location.ilike("%" + query + "%"))
            .order_by(LocationModel.population.desc())
            .limit(max)
            .all()
        )
        for entry in entries:
            if entry.location not in closest:
                closest.append(entry.location)
                if len(closest) >= max:
                    break

    return closest[:max]


def GazClosestMatches(query, max):
    alias = Alias(query)
    if alias:
        query = alias

    closest = []

    entries = (
        session.query(LocationModel.location)
        .filter(LocationModel.location.ilike("%" + query + "%"))
        .order_by(LocationModel.population.desc())
        .limit(max)
        .all()
    )
    closest.extend([(entry.location) for entry in entries])

    if len(closest) < max:
        entries = (
            session.query(func.lower(func.substr(LocationModel.location, 1, min(len(query), 15)))).distinct().all()
        )
        locations = [(entry[0]) for entry in entries]

        matches = difflib.get_close_matches(query, locations, max)
        # TODO remove any consecutive entries that are a subset of their preceding entry, e.g. Brugge, Brugg

        for match in matches:
            entries = (
                session.query(LocationModel.location)
                .filter(LocationModel.location.ilike(match + "%"))
                .order_by(LocationModel.population.desc())
                .limit(max)
                .all()
            )
            for entry in entries:
                if entry.location not in closest:
                    closest.append(entry.location)
                    if len(closest) >= max:
                        break

    if len(closest) < max:
        entries = session.query(LocationModel.location).order_by(LocationModel.population.desc()).limit(max).all()
        for entry in entries:
            if entry.location not in closest:
                closest.append(entry.location)
                if len(closest) >= max:
                    break

    return closest[:max]


def GazPlacename(location1, location2):
    if not location1:
        return None
    s1 = location1.split(", ")
    s2 = location2.split(", ")
    n1 = len(s1)
    n2 = len(s2)
    i = 1
    while i < n1 and i < n2 and s1[n1 - i] == s2[n2 - i]:
        i += 1
    return ", ".join(s1[0 : n1 - i + 1])


def GazCountry(location):
    s = location.split(", ")
    return s[-1]
