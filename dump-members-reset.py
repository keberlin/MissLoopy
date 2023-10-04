from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from mlutils import *
from model import *

session = db_init(MISSLOOPY_DB_URI)

session.query(AdminModel).update({"last_dump_member_search":datetime("2000-01-01 00:00:00"))
session.commit()
