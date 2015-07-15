#!/usr/bin/python

import database2

db = database2.Database('missloopy')

db.execute('DROP TABLE IF EXISTS profiles')

db.execute('''CREATE TABLE profiles (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE,
    password VARCHAR,
    created DATE,
    verified BOOLEAN DEFAULT False,
    last_login TIMESTAMP,
    name VARCHAR,
    gender INTEGER,
    dob DATE,
    height INTEGER,
    weight INTEGER,
    ethnicity INTEGER,
    education INTEGER,
    status INTEGER,
    smoking INTEGER,
    drinking INTEGER,
    country VARCHAR,
    region VARCHAR,
    placename VARCHAR,
    x INTEGER,
    y INTEGER,
    tz VARCHAR,
    occupation VARCHAR,
    summary VARCHAR,
    description VARCHAR,
    looking_for VARCHAR,
    gender_choice INTEGER,
    age_min INTEGER,
    age_max INTEGER,
    height_min INTEGER,
    height_max INTEGER,
    weight_choice INTEGER,
    ethnicity_choice INTEGER,
    location VARCHAR,
    last_ip VARCHAR,
    created2 TIMESTAMP,
    last_ip_country VARCHAR,
    notifications INTEGER DEFAULT 0
    )''')
db.execute('CREATE INDEX idx1 ON profiles (lower(email))')

db.execute('DROP TABLE IF EXISTS photos')

db.execute('CREATE TABLE photos (pid INTEGER PRIMARY KEY, id INTEGER, master BOOLEAN DEFAULT False)')
db.execute('CREATE INDEX idx2 ON photos (id)')

db.execute('DROP TABLE IF EXISTS emails')

db.execute('CREATE TABLE emails (id_from INTEGER, id_to INTEGER, message VARCHAR, sent TIMESTAMP, viewed BOOLEAN DEFAULT False)')
db.execute('CREATE INDEX idx3 ON emails (id_from, id_to)')

db.execute('DROP TABLE IF EXISTS blocked')

db.execute('CREATE TABLE blocked (id INTEGER, id_block INTEGER)')
db.execute('CREATE INDEX idx4 ON blocked (id, id_block)')

db.execute('DROP TABLE IF EXISTS favorites')

db.execute('CREATE TABLE favorites (id INTEGER, id_favorite INTEGER)')
db.execute('CREATE INDEX idx5 ON favorites (id, id_favorite)')

db.execute('DROP TABLE IF EXISTS results')

db.execute('CREATE TABLE results (id INTEGER, id_search INTEGER, id_previous INTEGER, id_next INTEGER)')
db.execute('CREATE INDEX idx6 ON results (id, id_search)')

db.execute('DROP TABLE IF EXISTS admin')

db.execute('CREATE TABLE admin (last_new_member_search TIMESTAMP, last_dump_member_search TIMESTAMP)')

db.commit()
