from datetime import datetime, timedelta
import time

from database import db_init, MISSLOOPY_DB_URI
from mlutils import *
from model import EmailModel
from utils import *

session = db_init(MISSLOOPY_DB_URI)

entries = (
    session.query(EmailModel.id_from, func.count(EmailModel.id_to.distinct()), func.min(EmailModel.sent))
    .group_by(EmailModel.id_from)
    .order_by(func.count(EmailModel.id_to.distinct()))
    .all()
)
for entry in entries:
    id_from = entry.id_from
    members = entry[1]
    if members < 5:
        continue
    count = entry[1]
    sent_min = entry[2]
    sent_max = datetime.utcnow()
    td = sent_max - sent_min
    seconds = td.days * 24 * 60 * 60 + td.seconds
    frequency = seconds / count
    td = timedelta(seconds=frequency)
    print("id:%d has sent %d messages to %d members, 1 every %s" % (id_from, count, members, TimeDiff(td)))
