import sqlite3

from mljson import *
from utils import *

conn2 = sqlite3.connect('gazetteer.db', detect_types=sqlite3.PARSE_DECLTYPES)
cursor2 = conn2.cursor()

sql = 'SELECT DISTINCT country FROM placenames'
cursor2.execute(sql)
countries = [(entry2[0]) for entry2 in cursor2.fetchall()]

Return({'countries':countries})

cursor2.close()
conn2.close()
