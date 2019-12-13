import argparse

import database

from utils import *
from mlutils import *
from emails import *

from logger import *

parser = argparse.ArgumentParser(description='Delete Members.')
parser.add_argument('id', nargs='+', help='member ids to be deleted')
args = parser.parse_args()

db = database.Database(MISS_LOOPY_DB)

for id in args.id:
  id = int(id)
  db.execute('SELECT * FROM profiles WHERE id=%d LIMIT 1' % (id))
  entry = db.fetchone()
  if not entry:
    continue
  ip = entry[COL_LAST_IP]
  email = entry[COL_EMAIL]
  name = entry[COL_NAME]
  db.execute("SELECT message, sent FROM emails WHERE id_from=%d ORDER BY sent DESC LIMIT 1" % (id))
  entry = db.fetchone()
  if not entry:
    continue
  message = entry[0]
  StopForumSpamAdd(name,email,ip,message)
  DeleteMember(id)
  EmailKicked(email)
  logger.info('Kicked %d %s' % (id, email))
