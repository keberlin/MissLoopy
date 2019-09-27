#!/usr/bin/python

import database

db = database.Database('missloopy')

db.execute('DROP TABLE IF EXISTS profiles')

db.execute('''CREATE TABLE profiles (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR UNIQUE,
    password VARCHAR,
    created DATE,
    verified BOOLEAN DEFAULT false,
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

db.execute('CREATE TABLE photos (pid BIGSERIAL PRIMARY KEY, id BIGINT, master BOOLEAN DEFAULT false)')
db.execute('CREATE INDEX idx2 ON photos (id)')

db.execute('DROP TABLE IF EXISTS emails')

db.execute('CREATE TABLE emails (id_from BIGINT, id_to BIGINT, message VARCHAR, sent TIMESTAMP, viewed BOOLEAN DEFAULT false)')
db.execute('CREATE INDEX idx3 ON emails (id_from, id_to)')

db.execute('DROP TABLE IF EXISTS blocked')

db.execute('CREATE TABLE blocked (id BIGINT, id_block BIGINT)')
db.execute('CREATE INDEX idx4 ON blocked (id, id_block)')

db.execute('DROP TABLE IF EXISTS favorites')

db.execute('CREATE TABLE favorites (id BIGINT, id_favorite BIGINT)')
db.execute('CREATE INDEX idx5 ON favorites (id, id_favorite)')

db.execute('DROP TABLE IF EXISTS results')

db.execute('CREATE TABLE results (id BIGINT, id_search BIGINT, id_previous BIGINT, id_next BIGINT)')
db.execute('CREATE INDEX idx6 ON results (id, id_search)')

db.execute('DROP TABLE IF EXISTS admin')

db.execute('CREATE TABLE admin (last_new_member_search TIMESTAMP, last_dump_member_search TIMESTAMP)')

db.commit()
