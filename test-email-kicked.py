from database import db_init
from emails import *

session = db_init()

email = "keith.hollis@gmail.com"

EmailKicked(session, email)
