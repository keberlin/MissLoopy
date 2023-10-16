import re

from database import db_init, MISSLOOPY_DB_URI
from mlutils import *
from model import *

session = db_init(MISSLOOPY_DB_URI)

entries = (
    session.query(EmailModel.id_from, EmailModel.message).filter(EmailModel.message.notlike("data:image/%%")).all()
)
for entry in entries:
    id_from = entry.id_from
    message = re.sub("[\r\n]+", " ", entry.message)
    print("%d %s" % (id_from, message))
