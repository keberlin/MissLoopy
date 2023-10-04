import csv

from sqlalchemy import create_engine

from database import MISSLOOPY_DB_URI, db_init
from mlutils import *
from model import *
from utils import *

session = db_init(MISSLOOPY_DB_URI)

def Null(v):
  if v: return Quote(v)
  return 'Null'

def Int(v):
  try:
    return str(int(v))
  except:
    return 'Null'

def Boolean(v):
  try:
    return 'True' if int(v) else 'False'
  except:
    return 'Null'

def Quoted(v):
  return Quote(v.decode('utf-8','ignore'))

print 'Processing profiles..'
with open('profiles.csv', 'rb') as input:
  reader = csv.reader(input)
  for entry in reader:
    sql = '''
      INSERT INTO profiles (id,email,password,verified,last_login,name,gender,dob,height,weight,ethnicity,education,status,smoking,drinking,x,y,tz,occupation,summary,description,looking_for,gender_choice,age_min,age_max,height_min,height_max,weight_choice,ethnicity_choice,location,last_ip,created2,last_ip_country,notifications)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''' % (
        Int(entry[COL_ID]),
        Quoted(entry[COL_EMAIL]),
        Quoted(entry[COL_PASSWORD]),
        Boolean(entry[COL_VERIFIED]),
        Null(entry[COL_LAST_LOGIN]),
        Quoted(entry[COL_NAME]),
        Int(entry[COL_GENDER]),
        Quoted(entry[COL_DOB]),
        Int(entry[COL_HEIGHT]),
        Int(entry[COL_WEIGHT]),
        Int(entry[COL_ETHNICITY]),
        Int(entry[COL_EDUCATION]),
        Int(entry[COL_STATUS]),
        Int(entry[COL_SMOKING]),
        Int(entry[COL_DRINKING]),
        Int(entry[COL_X]),
        Int(entry[COL_Y]),
        Quoted(entry[COL_TZ]),
        Quoted(entry[COL_OCCUPATION]),
        Quoted(entry[COL_SUMMARY]),
        Quoted(entry[COL_DESCRIPTION]),
        Quoted(entry[COL_LOOKING_FOR]),
        Int(entry[COL_GENDER_CHOICE]),
        Int(entry[COL_AGE_MIN]),
        Int(entry[COL_AGE_MAX]),
        Int(entry[COL_HEIGHT_MIN]),
        Int(entry[COL_HEIGHT_MAX]),
        Int(entry[COL_WEIGHT_CHOICE]),
        Int(entry[COL_ETHNICITY_CHOICE]),
        Quoted(entry[COL_LOCATION]),
        Quoted(entry[COL_LAST_IP]),
        Quoted(entry[COL_CREATED2]),
        Quoted(entry[COL_LAST_IP_COUNTRY]),
        Int(entry[COL_NOTIFICATIONS]))
    db.execute(sql)

print 'Processing photos..'
with open('photos.csv', 'rb') as input:
  reader = csv.reader(input)
  for entry in reader:
    sql = '''
      INSERT INTO photos (pid,id,master)
      VALUES (%s,%s,%s)''' % (
        Int(entry[COL3_PID]),
        Int(entry[COL3_ID]),
        Boolean(entry[COL3_MASTER]))
    db.execute(sql)

print 'Processing emails..'
with open('emails.csv', 'rb') as input:
  reader = csv.reader(input)
  for entry in reader:
    sql = '''
      INSERT INTO emails (id_from,id_to,message,sent,viewed)
      VALUES (%s,%s,%s,%s,%s)''' % (
        Int(entry[COL4_ID_FROM]),
        Int(entry[COL4_ID_TO]),
        Quoted(entry[COL4_MESSAGE]),
        Quoted(entry[COL4_SENT]),
        Boolean(entry[COL4_VIEWED]))
    db.execute(sql)

print 'Processing blocked..'
with open('blocked.csv', 'rb') as input:
  reader = csv.reader(input)
  for entry in reader:
    sql = '''
      INSERT INTO blocked (id,id_block)
      VALUES (%s,%s)''' % (
        Int(entry[COL6_ID]),
        Int(entry[COL6_ID_BLOCK]))
    db.execute(sql)

print 'Processing favorites..'
with open('favorites.csv', 'rb') as input:
  reader = csv.reader(input)
  for entry in reader:
    sql = '''
      INSERT INTO favorites (id,id_favorite)
      VALUES (%s,%s)''' % (
        Int(entry[COL7_ID]),
        Int(entry[COL7_ID_FAVORITE]))
    db.execute(sql)

print 'Processing results..'
with open('results.csv', 'rb') as input:
  reader = csv.reader(input)
  for entry in reader:
    sql = '''
      INSERT INTO results (id,id_search,id_previous,id_next)
      VALUES (%s,%s,%s,%s)''' % (
        Int(entry[COL5_ID]),
        Int(entry[COL5_ID_SEARCH]),
        Int(entry[COL5_ID_PREVIOUS]),
        Int(entry[COL5_ID_NEXT]))
    db.execute(sql)

print 'Processing admin..'
with open('admin.csv', 'rb') as input:
  reader = csv.reader(input)
  for entry in reader:
    sql = '''
      INSERT INTO admin (last_new_member_search,last_dump_member_search)
      VALUES (%s,%s)''' % (
        Quoted(entry[0]),
        Quoted(entry[1]))
    db.execute(sql)
    break

db.commit()
