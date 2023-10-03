from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import MISSLOOPY_DB_URI, db
from mlutils import *
from model import *

engine = create_engine(MISSLOOPY_DB_URI)
Session = sessionmaker(bind=engine)
db.session = Session()

db.session.query(AdminModel).update({"last_dump_member_search":datetime("2000-01-01 00:00:00"))
db.session.commit()
