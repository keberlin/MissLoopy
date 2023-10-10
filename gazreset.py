from database import GAZETTEER_DB

db = database.Database(GAZETTEER_DB)

db.execute(
    "CREATE TABLE locations (location VARCHAR PRIMARY KEY NOT NULL, x INTEGER, y INTEGER, tz VARCHAR, population INTEGER)"
)

db.execute("CREATE INDEX idx1 ON locations (location)")

db.commit()
