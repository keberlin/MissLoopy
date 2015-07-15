import sqlite3

databases = {}

class Database():
  def __init__(self, name):
    global databases
    if name not in databases:
      conn = sqlite3.connect(name, detect_types=sqlite3.PARSE_DECLTYPES, timeout=60)
      cursor = conn.cursor()
      databases[name] = (conn, cursor)
    self.conn, self.cursor = databases[name]
  def __del__(self):
    global databases
    if False:
      cursor.close()
      cursor = None
      conn.close()
      conn = None
  def execute(self,sql):
    self.cursor.execute(sql)
    self.lastrowid = self.cursor.lastrowid
  def fetchone(self):
    return self.cursor.fetchone()
  def fetchall(self):
    return self.cursor.fetchall()
  def commit(self):
    return self.conn.commit()
