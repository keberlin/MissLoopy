from localization import *
from mlutils import *
from emails import *

db = database.Database(MISS_LOOPY_DB)

db.execute("SELECT * FROM profiles WHERE email ILIKE 'keith.hollis@gmail.com' LIMIT 1")
entry = db.fetchone()

db.execute("SELECT * FROM profiles WHERE email ILIKE 'razeberlin@gmail.com' LIMIT 1")
entry_to = db.fetchone()

EmailNotify(entry_to, entry)
