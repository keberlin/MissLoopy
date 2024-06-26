from datetime import datetime, timedelta

from database import db_init
from mlutils import *
from model import *
from utils import *

session = db_init()

now = datetime.utcnow()
since = now - timedelta(days=30)

count = 0
entries = (
    session.query(ProfileModel).filter(ProfileModel.verified.is_(True)).filter(ProfileModel.created >= since).all()
)
for entry in entries:
    id = entry.id
    name = entry.name
    dob = entry.dob
    location = entry.location
    gender = entry.gender
    ethnicity = entry.ethnicity
    last_ip = entry.last_ip
    last_ip_country = entry.last_ip_country

    out = "id:%d (%s) %s %d (%s) %s (%s)" % (id, name, Gender(gender), Age(dob), dob, location, last_ip_country)
    print(out)

    count += 1

if count:
    td = now - since
    seconds = td.days * 24 * 60 * 60 + td.seconds
    td = timedelta(seconds=seconds / count)
    print(
        "%d new members since %s, 1 every %s, %d per day"
        % (count, str(since), TimeDiff(td), count * 24 * 60 * 60 / seconds)
    )
else:
    print("No new members since %s" % (str(since)))
