from database import db_init
from emails import *
from localization import *
from mlutils import *

session = db_init()

profile_id = 1
pid = 1
filename = PhotoFilename(pid)

EmailNewPhoto(session, filename, pid, profile_id)
