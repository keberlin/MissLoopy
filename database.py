from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MISSLOOPY_DB_URI = "postgresql://postgres:postgres@localhost:5432/missloopy?client_encoding=utf8"
GAZETTEER_DB_URI = "postgresql://postgres:postgres@localhost:5432/gazetteer?client_encoding=utf8"
IPADDRESS_DB_URI = "postgresql://postgres:postgres@localhost:5432/ipaddress?client_encoding=utf8"


db = SQLAlchemy()


def db_init(uri=MISSLOOPY_DB_URI):
    engine = create_engine(uri)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
