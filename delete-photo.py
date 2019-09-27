#!/usr/bin/python

import argparse

import database

from mlutils import *
from emails import *

parser = argparse.ArgumentParser(description='Delete Photos.')
parser.add_argument('pid', nargs='+', help='photo ids to be deleted')
args = parser.parse_args()

db = database.Database(MISS_LOOPY_DB)

for pid in args.pid:
  db.execute('SELECT id FROM photos WHERE pid=%d' % int(pid))
  entry = db.fetchone()
  id = int(entry[0])
  db.execute('SELECT * FROM profiles WHERE id=%d' % (id))
  entry = db.fetchone()
  email = entry[COL_EMAIL]
  DeletePhoto(int(pid))
  EmailPhotoDeleted(email)
