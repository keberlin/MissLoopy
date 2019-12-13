from localization import *
from mlutils import *
from emails import *

db = database.Database(MISS_LOOPY_DB)

db.execute("SELECT * FROM profiles WHERE email ILIKE 'keith.hollis@gmail.com' LIMIT 1")
entry = db.fetchone()

members = [15, 18, 25, 27, 35]

EmailNewMembers(entry, members)
