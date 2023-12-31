from datetime import datetime
import re
import time

from sqlalchemy.sql.expression import func

from database import db
from mlutils import *
from model import *


def AnalyseSpammer(id):
    entry = (
        db.session.query(func.count(EmailModel.id_to.distinct()), func.count(), func.min(EmailModel.sent))
        .filter(EmailModel.id_from == id)
        .one()
    )
    members = entry[0]
    count = entry[1]
    if count == 0:
        return (0, 0)
    sent_min = entry[2]
    sent_max = datetime.utcnow()
    td = sent_max - sent_min
    frequency = (td.days * 24 * 60 * 60 + td.seconds) / count
    return (members, frequency)


def AnalyseSpam(text):
    score = 0
    hits = []
    entries = db.session.query(SpamModel).all()
    for entry in entries:
        matches = re.findall(re.sub(r" +", r"\W+", entry.str), text, re.IGNORECASE)  # Treat all whitespace the same
        if matches:
            score += entry.cost * len(matches)
            hits.append(entry.str)
    density = len(text) / float(score) if score else 0
    return (score, density, hits)


def IsSpamFactored(tuple, spammer, mult=1):
    score, density, hits = tuple
    members, frequency = spammer
    hours = frequency / (60 * 60)
    if hours < 1:
        factor = 0.25
    elif hours < 2:
        factor = 0.20
    elif hours < 4:
        factor = 0.15
    elif hours < 6:
        factor = 0.10
    elif hours < 8:
        factor = 0.05
    else:
        factor = 0
    density /= 1 + factor * members
    return (density and density < 20 * mult) or (members >= 25 and hours < 1)
