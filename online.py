from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import MISSLOOPY_DB_URI, db
from mlutils import *
from model import *
from utils import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

now = datetime.datetime.utcnow()

# Count online users (active within the last hour)
count = db.session.query(func.count(ProfileModel.id)).filter(ProfileModel.verified.is_(True),ProfileModel.last_login>=now-datetime.timedelta(hours=1)).scalar()
print 'Users online: %d' % count
