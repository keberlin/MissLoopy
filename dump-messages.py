import re

from database import db_init
from mlutils import *
from model import EmailModel

session = db_init()

entries = (
    session.query(EmailModel.id_from, EmailModel.message)
    .filter(EmailModel.message.notlike("data:image/%%"))
    .order_by(EmailModel.sent)
    .distinct()
    .all()
)
for entry in entries:
    id_from = entry.id_from
    message = re.sub("[\r\n]+", " ", entry.message)
    print("%d %s" % (id_from, message))
