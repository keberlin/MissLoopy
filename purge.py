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

# Delete any unverified profiles after 1 month
td = now-datetime.timedelta(days=30)
db.session.delete(ProfileModel).filter(ProfileModel.verified.is_(False),ProfileModel.created2<td)
db.session.commit()

# Delete all emails older than 6 months
td = now-datetime.timedelta(days=30*6)
db.session.delete(EmailModel).filter(EmailModel.sent<td)
db.session.commit()
