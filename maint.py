import database, re, hashlib

from utils import *
from mlutils import *

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT * FROM profiles WHERE id=1')
for entry in db.fetchall():
  print(entry[COL_PASSWORD], entry[COL_PASSWORD].encode(), hashlib.md5(entry[COL_PASSWORD].encode()).hexdigest())
  #db.execute('UPDATE profiles SET password=%s WHERE id=%d' % (Quote(hashlib.md5(entry[COL_PASSWORD].encode()).hexdigest()), entry[COL_ID]))

db.commit()
