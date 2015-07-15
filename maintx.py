#!/usr/bin/python

import sqlite3

from utils import *
from iputils import *

conn = sqlite3.connect('missloopy.db', detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()

cursor.execute('ALTER TABLE profiles ADD COLUMN notifications DEFAULT 0')
conn.commit()

cursor.close()
conn.close()
