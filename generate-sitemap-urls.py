from database import db_init, MISSLOOPY_DB_URI
from model import ProfileModel

session = db_init(MISSLOOPY_DB_URI)
entries = session.query(ProfileModel.id).filter(ProfileModel.verified.is_(True)).all()

with open("web_urls.txt", "w") as f:
    for entry in entries:
        url = f"http://www.missloopy.com/member?id={entry.id}"
        f.write(url + "\n")
