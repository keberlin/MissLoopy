import re

from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from mlutils import *
from model import *

db = db_init(MISSLOOPY_DB_URI)

entries = db.session.query(EmailModel.id_from,EmailModel.message).filter(EmailModel.message.notlike('data:image/%%')).all()
for entry in entries:
  id_from = entry.id_from
  message = re.sub('[\r\n]+',' ',entry.message)
  print '%d %s' % (id_from, message.encode('utf-8'))
