from database import db_init
from model import AdminModel

session = db_init()

session.query(AdminModel).update({"last_dump_member_search": datetime("2000-01-01 00:00:00")})
session.commit()
