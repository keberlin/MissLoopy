from database import IP_ADDRESS_DB

db = database.Database(IP_ADDRESS_DB)

db.execute("CREATE TABLE ranges (lower BIGINT NOT NULL, upper BIGINT NOT NULL, country VARCHAR)")

db.execute("CREATE INDEX idx1 ON ranges (lower)")
db.execute("CREATE INDEX idx2 ON ranges (upper)")

db.commit()
