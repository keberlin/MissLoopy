from database import db


class ProfileModel(db.Model):
    __tablename__ = "profiles"
    #__table_args__ = {"schema":"missloopy"}
    #__unique__ = "email"

    id = db.Column("id", db.Integer, primary_key=True, server_default=db.Identity(), nullable=False)
    email = db.Column("email", db.String, nullable=False)
    password = db.Column("password", db.String, nullable=False)
    created = db.Column("created", db.DateTime)
    created2 = db.Column("created2", db.DateTime, nullable=False)
    verified = db.Column("verified", db.Boolean, default=False)
    last_login = db.Column("last_login", db.DateTime)
    name = db.Column("name", db.String)
    gender = db.Column("gender", db.Integer)
    dob = db.Column("dob", db.Date)
    height = db.Column("height", db.Integer)
    weight = db.Column("weight", db.Integer)
    ethnicity = db.Column("ethnicity", db.Integer)
    education = db.Column("education", db.Integer)
    status = db.Column("status", db.Integer)
    smoking = db.Column("smoking", db.Integer)
    drinking = db.Column("drinking", db.Integer)
    country = db.Column("country", db.String)
    region = db.Column("region", db.String)
    placename = db.Column("placename", db.String)
    x = db.Column("x", db.Integer)
    y = db.Column("y", db.Integer)
    tz = db.Column("tz", db.String)
    occupation = db.Column("occupation", db.String)
    summary = db.Column("summary", db.String)
    description = db.Column("description", db.String)
    looking_for = db.Column("looking_for", db.String)
    gender_choice = db.Column("gender_choice", db.Integer)
    age_min = db.Column("age_min", db.Integer)
    age_max = db.Column("age_max", db.Integer)
    height_min = db.Column("height_min", db.Integer)
    height_max = db.Column("height_max", db.Integer)
    weight_choice = db.Column("weight_choice", db.Integer)
    ethnicity_choice = db.Column("ethnicity_choice", db.Integer)
    location = db.Column("location", db.String)
    last_ip = db.Column("last_ip", db.String)
    last_ip_country = db.Column("last_ip_country", db.String)
    notifications = db.Column("notifications", db.Integer, default=0)

class PhotoModel(db.Model):
    __tablename__ = "photos"

    pid = db.Column("pid", db.Integer, primary_key=True, server_default=db.Identity(), nullable=False)
    id = db.Column("id", db.Integer, db.ForeignKey(ProfileModel.id), nullable=False)
    sequence = db.Column("sequence", db.Integer, default=0)
    master = db.Column("master", db.Boolean, default=False)
    created = db.Column("created", db.DateTime)

class EmailModel(db.Model):
    __tablename__ = "emails"

    id_from = db.Column("id_from", db.Integer, primary_key=True, nullable=False)
    id_to = db.Column("id_to", db.Integer, db.ForeignKey(ProfileModel.id), nullable=False)
    message = db.Column("message", db.String)
    sent = db.Column("sent", db.DateTime)
    viewed = db.Column("viewed", db.Boolean, default=False)
    image = db.Column("image", db.String)

class BlockedModel(db.Model):
    __tablename__ = "blocked"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    id_block = db.Column("id_block", db.Integer, db.ForeignKey(ProfileModel.id), nullable=False)

class FavoriteModel(db.Model):
    __tablename__ = "favorites"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    id_favorite = db.Column("id_favorite", db.Integer, db.ForeignKey(ProfileModel.id), nullable=False)

class ResultModel(db.Model):
    __tablename__ = "results"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    id_search = db.Column("id_search", db.Integer, db.ForeignKey(ProfileModel.id), nullable=False)
    id_previous = db.Column("id_previous", db.Integer, db.ForeignKey(ProfileModel.id), nullable=False)
    id_next = db.Column("id_next", db.Integer, db.ForeignKey(ProfileModel.id), nullable=False)

class AdminModel(db.Model):
    __tablename__ = "admin"

    last_new_member_search = db.Column("last_new_member_search", db.DateTime, primary_key=True)
    last_dump_member_search = db.Column("last_dump_member_search", db.DateTime)

class ReportModel(db.Model):
    __tablename__ = "reports"

    logged = db.Column("logged", db.DateTime, primary_key=True, nullable=False)
    verified = db.Column("verified", db.Integer)
    unverified = db.Column("unverified", db.Integer)
    males = db.Column("males", db.Integer)
    females = db.Column("females", db.Integer)
    men = db.Column("men", db.Integer)
    women = db.Column("women", db.Integer)
    sugar_pups = db.Column("sugar_pups", db.Integer)
    sugar_babies = db.Column("sugar_babies", db.Integer)
    sugar_daddies = db.Column("sugar_daddies", db.Integer)
    sugar_mommas = db.Column("sugar_mommas", db.Integer)
    avg_age_males = db.Column("avg_age_males", db.Float)
    avg_age_females = db.Column("avg_age_females", db.Float)
    avg_age_men = db.Column("avg_age_men", db.Float)
    avg_age_women = db.Column("avg_age_women", db.Float)
    avg_age_sugar_pups = db.Column("avg_age_sugar_pups", db.Float)
    avg_age_sugar_babies = db.Column("avg_age_sugar_babies", db.Float)
    avg_age_sugar_daddies = db.Column("avg_age_sugar_daddies", db.Float)
    avg_age_sugar_mommas = db.Column("avg_age_sugar_mommas", db.Float)
    white = db.Column("white", db.Integer)
    black = db.Column("black", db.Integer)
    latino = db.Column("latino", db.Integer)
    indian = db.Column("indian", db.Integer)
    asian = db.Column("asian", db.Integer)
    mixed = db.Column("mixed", db.Integer)
    other = db.Column("other", db.Integer)
    active = db.Column("active", db.Integer)
    messages = db.Column("messages", db.Integer)

class SpamModel(db.Model):
    __tablename__ = "spam"

    str = db.Column("str", db.String, primary_key=True, nullable=False)
    cost = db.Column("cost", db.Float, nullable=False)
