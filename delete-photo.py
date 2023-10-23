import argparse

from database import db_init, MISSLOOPY_DB_URI
from emails import *
from mlutils import *
from model import *

logging.basicConfig(filename="/var/log/missloopy/log", level=logging.INFO)

session = db_init(MISSLOOPY_DB_URI)

parser = argparse.ArgumentParser(description="Delete Photos.")
parser.add_argument("pid", nargs="+", help="photo ids to be deleted")
args = parser.parse_args()

for pid in args.pid:
    pid = int(pid)
    entry = session.query(EmailModel.id).filter(PhotoModel.pid == pid).one()
    id = entry.id
    entry = session.query(ProfileModel.email).filter(ProfileModel.id == id).one()
    email = entry.email
    DeletePhoto(session, pid)
    EmailPhotoDeleted(email)
