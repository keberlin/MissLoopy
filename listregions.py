import cgi
import sqlite3

from mljson import *
from utils import *

conn2 = sqlite3.connect("gazetteer.db", detect_types=sqlite3.PARSE_DECLTYPES)
cursor2 = conn2.cursor()

form = cgi.FieldStorage()
dict = dict([(field, form.getvalue(field)) for field in list(form.keys())])

if not "country" in dict:
    Error("No country specified.")

country = dict["country"]

sql = "SELECT DISTINCT region FROM placenames WHERE country=%s" % (Quote(country))
cursor2.execute(sql)
regions = [(entry2[0]) for entry2 in cursor2.fetchall()]

Return({"regions": regions})

cursor2.close()
conn2.close()
