from datetime import datetime, timedelta

from database import db_init
from mlutils import *
from model import *
from utils import *

session = db_init()

now = datetime.utcnow()

# Count online users (active within the last hour)
count = (
    session.query(func.count(ProfileModel.id))
    .filter(ProfileModel.verified.is_(True), ProfileModel.last_login >= now - timedelta(hours=1))
    .scalar()
)
print("Users online: %d" % count)
