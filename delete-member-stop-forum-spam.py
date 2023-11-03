import argparse

from database import db_init, MISSLOOPY_DB_URI
from emails import EmailKicked
from logger import logger
from mlutils import DeleteMember
from model import EmailModel, ProfileModel
from urlutils import StopForumSpamAdd

session = db_init(MISSLOOPY_DB_URI)

parser = argparse.ArgumentParser(description="Delete Members.")
parser.add_argument("id", nargs="+", help="member ids to be deleted")
args = parser.parse_args()

for id in args.id:
    profile_id = int(id)
    entry = session.query(ProfileModel).filter(ProfileModel.id == profile_id).one_or_none()
    if not entry:
        continue
    ip = entry.last_ip
    email = entry.email
    name = entry.name
    entry = (
        session.query(EmailModel.message)
        .filter(EmailModel.id_from == profile_id)
        .order_by(EmailModel.sent.desc())
        .first()
    )
    if not entry:
        continue
    message = entry.message
    StopForumSpamAdd(name, email, ip, message)
    DeleteMember(session, profile_id)
    EmailKicked(email)
    logger.info(f"Kicked {profile_id} {email}")
