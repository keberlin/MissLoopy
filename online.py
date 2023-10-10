from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from mlutils import *
from model import *
from utils import *

session = db_init(MISSLOOPY_DB_URI)

now = datetime.datetime.utcnow()

# Count online users (active within the last hour)
count = (
    session.query(func.count(ProfileModel.id))
    .filter(ProfileModel.verified.is_(True), ProfileModel.last_login >= now - datetime.timedelta(hours=1))
    .scalar()
)
print("Users online: %d" % count)
