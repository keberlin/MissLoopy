from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Float, ForeignKey, Identity, Integer, String

from database import db

# DB missloopy


class ProfileModel(db.Model):
    __tablename__ = "profiles"
    # __table_args__ = {"schema":"missloopy"}
    # __unique__ = "email"

    id = Column("id", Integer, primary_key=True, server_default=Identity(), nullable=False)
    email = Column("email", String, nullable=False)
    password = Column("password", String, nullable=False)
    created = Column("created", DateTime)
    created2 = Column("created2", DateTime, nullable=False)
    verified = Column("verified", Boolean, default=False)
    last_login = Column("last_login", DateTime)
    name = Column("name", String)
    gender = Column("gender", Integer)
    dob = Column("dob", Date)
    height = Column("height", Integer)
    weight = Column("weight", Integer)
    ethnicity = Column("ethnicity", Integer)
    education = Column("education", Integer)
    status = Column("status", Integer)
    smoking = Column("smoking", Integer)
    drinking = Column("drinking", Integer)
    country = Column("country", String)
    region = Column("region", String)
    placename = Column("placename", String)
    x = Column("x", Integer)
    y = Column("y", Integer)
    tz = Column("tz", String)
    occupation = Column("occupation", String)
    summary = Column("summary", String)
    description = Column("description", String)
    looking_for = Column("looking_for", String)
    gender_choice = Column("gender_choice", Integer)
    age_min = Column("age_min", Integer)
    age_max = Column("age_max", Integer)
    height_min = Column("height_min", Integer)
    height_max = Column("height_max", Integer)
    weight_choice = Column("weight_choice", Integer)
    ethnicity_choice = Column("ethnicity_choice", Integer)
    location = Column("location", String)
    last_ip = Column("last_ip", String)
    last_ip_country = Column("last_ip_country", String)
    notifications = Column("notifications", Integer, default=0)


class PhotoModel(db.Model):
    __tablename__ = "photos"

    pid = Column("pid", Integer, primary_key=True, server_default=Identity(), nullable=False)
    id = Column("id", Integer, ForeignKey(ProfileModel.id), nullable=False)
    sequence = Column("sequence", Integer, default=0)
    master = Column("master", Boolean, default=False)
    created = Column("created", DateTime)


class EmailModel(db.Model):
    __tablename__ = "emails"

    id_from = Column("id_from", Integer, primary_key=True, nullable=False)
    id_to = Column("id_to", Integer, ForeignKey(ProfileModel.id), nullable=False)
    message = Column("message", String)
    sent = Column("sent", DateTime)
    viewed = Column("viewed", Boolean, default=False)
    image = Column("image", String)


class BlockedModel(db.Model):
    __tablename__ = "blocked"

    id = Column("id", Integer, primary_key=True, nullable=False)
    id_block = Column("id_block", Integer, ForeignKey(ProfileModel.id), nullable=False)


class FavoriteModel(db.Model):
    __tablename__ = "favorites"

    id = Column("id", Integer, primary_key=True, nullable=False)
    id_favorite = Column("id_favorite", Integer, ForeignKey(ProfileModel.id), nullable=False)


class ResultModel(db.Model):
    __tablename__ = "results"

    id = Column("id", Integer, primary_key=True, nullable=False)
    id_search = Column("id_search", Integer, ForeignKey(ProfileModel.id), nullable=False)
    id_previous = Column("id_previous", Integer, ForeignKey(ProfileModel.id), nullable=False)
    id_next = Column("id_next", Integer, ForeignKey(ProfileModel.id), nullable=False)


class AdminModel(db.Model):
    __tablename__ = "admin"

    last_new_member_search = Column("last_new_member_search", DateTime, primary_key=True)
    last_dump_member_search = Column("last_dump_member_search", DateTime)


class ReportModel(db.Model):
    __tablename__ = "reports"

    logged = Column("logged", DateTime, primary_key=True, nullable=False)
    verified = Column("verified", Integer)
    unverified = Column("unverified", Integer)
    males = Column("males", Integer)
    females = Column("females", Integer)
    men = Column("men", Integer)
    women = Column("women", Integer)
    sugar_pups = Column("sugar_pups", Integer)
    sugar_babies = Column("sugar_babies", Integer)
    sugar_daddies = Column("sugar_daddies", Integer)
    sugar_mommas = Column("sugar_mommas", Integer)
    avg_age_males = Column("avg_age_males", Float)
    avg_age_females = Column("avg_age_females", Float)
    avg_age_men = Column("avg_age_men", Float)
    avg_age_women = Column("avg_age_women", Float)
    avg_age_sugar_pups = Column("avg_age_sugar_pups", Float)
    avg_age_sugar_babies = Column("avg_age_sugar_babies", Float)
    avg_age_sugar_daddies = Column("avg_age_sugar_daddies", Float)
    avg_age_sugar_mommas = Column("avg_age_sugar_mommas", Float)
    white = Column("white", Integer)
    black = Column("black", Integer)
    latino = Column("latino", Integer)
    indian = Column("indian", Integer)
    asian = Column("asian", Integer)
    mixed = Column("mixed", Integer)
    other = Column("other", Integer)
    active = Column("active", Integer)
    messages = Column("messages", Integer)


class SpamModel(db.Model):
    __tablename__ = "spam"

    str = Column("str", String, primary_key=True, nullable=False)
    cost = Column("cost", Float, nullable=False)


# DB gazetteer


class LocationModel(db.Model):
    __tablename__ = "locations"

    location = Column("location", String, primary_key=True, nullable=False)
    x = Column("x", Integer, nullable=False)
    y = Column("y", Integer, nullable=False)
    tz = Column("tz", String, nullable=False)
    population = Column("population", Integer)


# DB ipaddress


class RangeModel(db.Model):
    __tablename__ = "ranges"

    # uid = Column("uid", Integer, Identity(), primary_key=True, nullable=False)
    lower = Column("lower", BigInteger, primary_key=True, nullable=False)
    upper = Column("upper", BigInteger, nullable=False)
    country = Column("country", String, nullable=False)
