#!/usr/bin/python

from localization import *
from mlutils import *
from emails import *

db = database.Database(MISS_LOOPY_DB)

db.execute('SELECT * FROM profiles WHERE email LIKE "keith.hollis@gmail.com" LIMIT 1')
entry = db.fetchone()

email    = entry[COL_EMAIL]
location = entry[COL_LOCATION]
country  = GazCountry(location)
x        = entry[COL_X]
y        = entry[COL_Y]
tz       = entry[COL_TZ]

SetLocale(country)

unit_distance, unit_height = Units(country)

EmailNotify(email, 2, x, y, tz, unit_distance)
