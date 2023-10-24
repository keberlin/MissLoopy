from database import db_init, MISSLOOPY_DB_URI
from emails import *

session = db_init(MISSLOOPY_DB_URI)

email = "keith.hollis@gmail.com"

EmailPhotoDeleted(session, email)
