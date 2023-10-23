# Database: missloopy

DROP TABLE IF EXISTS profiles;
DROP TABLE IF EXISTS photos;
DROP TABLE IF EXISTS emails;
DROP TABLE IF EXISTS blocked;
DROP TABLE IF EXISTS favorites;
DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS spam;

# Profiles

CREATE TABLE profiles (
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
);
CREATE INDEX idx1 ON profiles (lower(email));

# Photos

CREATE TABLE photos (pid BIGSERIAL PRIMARY KEY, id BIGINT, master BOOLEAN DEFAULT false);
CREATE INDEX idx2 ON photos (id);

# Emails

CREATE TABLE emails (id_from BIGINT, id_to BIGINT, message VARCHAR, sent TIMESTAMP, viewed BOOLEAN DEFAULT false);
CREATE INDEX idx3 ON emails (id_from, id_to);

# Blocked

CREATE TABLE blocked (id BIGINT, id_block BIGINT);
CREATE INDEX idx4 ON blocked (id, id_block);

# Favorites

CREATE TABLE favorites (id BIGINT, id_favorite BIGINT);
CREATE INDEX idx5 ON favorites (id, id_favorite);

# Results

CREATE TABLE results (id BIGINT, id_search BIGINT, id_previous BIGINT, id_next BIGINT);
CREATE INDEX idx6 ON results (id, id_search);

# Admin

CREATE TABLE admin (last_new_member_search TIMESTAMP, last_dump_member_search TIMESTAMP);
INSERT INTO admin (last_new_member_search,last_dump_member_search) VALUES("2014-01-01 00:00:00","2014-01-01 00:00:00")

# Reports

CREATE TABLE reports (
    logged TIMESTAMP, 
    verified INTEGER, 
    unverified INTEGER, 
    males INTEGER, 
    females INTEGER, 
    men INTEGER,
    women INTEGER,
    sugar_pups INTEGER, 
    sugar_babies INTEGER, 
    sugar_daddies INTEGER, 
    sugar_mommas INTEGER, 
    avg_age_males FLOAT, 
    avg_age_females FLOAT, 
    avg_age_men FLOAT, 
    avg_age_women FLOAT, 
    avg_age_sugar_pups FLOAT, 
    avg_age_sugar_babies FLOAT, 
    avg_age_sugar_daddies FLOAT, 
    avg_age_sugar_mommas FLOAT, 
    white INTEGER, 
    black INTEGER, 
    latino INTEGER, 
    indian INTEGER, 
    asian INTEGER, 
    mixed INTEGER, 
    other INTEGER, 
    active INTEGER, 
    messages INTEGER
);

# Spam

CREATE TABLE spam (str VARCHAR, cost FLOAT);

# UUIDs

CREATE TABLE uuids (uuid UUID PRIMARY KEY NOT NULL, profile_id INTEGER NOT NULL, expiry TIMESTAMP NOT NULL);

COMMIT;


# Database: gazatteer

CREATE TABLE locations (location VARCHAR PRIMARY KEY NOT NULL, x INTEGER, y INTEGER, tz VARCHAR, population INTEGER);

CREATE INDEX idx1 ON locations (location);

COMMIT;


# Database: ipaddress

CREATE TABLE ranges (lower BIGINT NOT NULL, upper BIGINT NOT NULL, country VARCHAR);

CREATE INDEX idx1 ON ranges (lower);
CREATE INDEX idx2 ON ranges (upper);

COMMIT;
