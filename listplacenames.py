import cgi
import sqlite3

from mljson import *
from utils import *

conn2 = sqlite3.connect('gazetteer.db', detect_types=sqlite3.PARSE_DECLTYPES)
cursor2 = conn2.cursor()

form = cgi.FieldStorage()
dict = dict([(field,form.getvalue(field)) for field in form.keys()])

if not 'country' in dict:
    Error('No country specified.')
if not 'region' in dict:
    Error('No region specified.')

country = dict['country']
region  = dict['region']

sql = 'SELECT DISTINCT placename FROM placenames WHERE country=%s AND region=%s' % (Quote(country), Quote(region))
cursor2.execute(sql)
placenames = [(entry2[0]) for entry2 in cursor2.fetchall()]

Return({'placenames':placenames})

cursor2.close()
conn2.close()
