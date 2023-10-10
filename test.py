import psycopg2

import database
from mlutils import *


def check_if_user_exists(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT email from profiles WHERE id=1")
    return cursor.fetchone() is not None


conn = psycopg2.connect(database=MISS_LOOPY_DB, user="postgres")
cursor = conn.cursor()

print(check_if_user_exists(conn))

cursor.execute("SELECT email from profiles WHERE id=1")
print(cursor.fetchone())
