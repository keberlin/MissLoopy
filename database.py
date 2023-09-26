from flask_sqlalchemy import SQLAlchemy

import psycopg2

#psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
#psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

MISSLOOPY_DB_URI = "postgresql://postgres:postgres@localhost:5432/missloopy?client_encoding=utf8"

class Database():
  databases = {}

  def __init__(self, name):
    if name not in self.databases:
      conn = psycopg2.connect(database=name, user='postgres')
      cursor = conn.cursor()
      self.databases[name] = (conn, cursor)
    self.conn, self.cursor = self.databases[name]
  def __del__(self):
    if False:
      cursor.close()
      cursor = None
      conn.close()
      conn = None
  def execute(self,sql,*nargs):
    self.cursor.execute(sql.encode('utf-8'),*nargs)
  def lastval(self):
      self.execute('SELECT LASTVAL()')
      return self.fetchone()[0]
  def fetchone(self):
    #return self.cursor.fetchone()
    entry = self.cursor.fetchone()
    if not entry:
      return None
    return map(lambda x:x.decode('utf-8','ignore') if isinstance(x,str) else x,entry)
  def fetchall(self):
    #return self.cursor.fetchall()
    for entry in self.cursor.fetchall():
      yield map(lambda x:x.decode('utf-8','ignore') if isinstance(x,str) else x,entry)
  def rollback(self):
    return self.conn.rollback()
  def commit(self):
    return self.conn.commit()

db = SQLAlchemy()
