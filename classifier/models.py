from datetime import datetime
from classifier import db, login_manager, bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


classifications = db.Table("classifications",
                           db.Column("image_id",db.Integer,db.ForeignKey("image.id"), primary_key=True),
                           db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
                           )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    qualifications = db.Column(db.String(1000), nullable=False)
    expertise = db.Column(db.String(2), nullable=False, default=0)
    #expertise = db.Column(db.Integer, nullable=False,default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(100), )

    images = db.relationship("Image", secondary="classifications", lazy='subquery',
                             backref=db.backref("users", lazy=True))

    def __init__(self, email=email, qualifications=qualifications, expertise=expertise,
                 password=password):
        self.email = email
        self.qualifications = qualifications
        self.expertise = expertise
        temp = password
        if not temp:
            temp = "password"
        hashed_password = bcrypt.generate_password_hash(temp).decode('utf-8')
        self.password = hashed_password

    def __repr__(self):
        return "User({},{})".format(self.email, self.expertise)

class Image(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(50), nullable=False)
    downloaded_name = db.Column(db.String(100), nullable=False)
    uri = db.Column(db.String(100), nullable=False)
    is_male = db.Column(db.Integer, nullable=True)
    is_juvenile = db.Column(db.Integer, nullable=True)
    is_standard = db.Column(db.Boolean, default=False)
    quality_of_image = db.Column(db.Integer, nullable=True)
    certainty = db.Column(db.Integer, nullable=True)
    total_expertise = db.Column(db.Integer, nullable=True)
    total_certainty = db.Column(db.Integer, nullable=True)
    is_classified = db.Column(db.Boolean, nullable=False, default=False)
    date_downloaded = db.Column(db.DateTime, default=datetime.utcnow)
    num_classifications= db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, species, downloaded_name, uri):
        self.species = species
        self.downloaded_name = downloaded_name
        self.uri = uri

    def __repr__(self):
        return f"Image({self.downloaded_name}, {self.uri})"


class Bird(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Scientific_Name = db.Column(db.String(100))
    Pop_Global = db.Column(db.Integer)
    Pop_US_Canada = db.Column(db.Integer)
    Pop_Canada = db.Column(db.Integer)
    Pop_USA = db.Column(db.Integer)
    Max_NA_Pop = db.Column(db.Integer)
    downloaded = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, scientific_name):
        self.Name = name,
        self.Scientific_Name = scientific_name

    def __repr__(self):
        return f"Bird({self.Name}, {self.Scientific_Name})"
