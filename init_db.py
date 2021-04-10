from classifier import create_app, db, bcrypt
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from classifier.models import User, Image, Bird

app = create_app()

with app.app_context():
    db.create_all()
    db.session.commit()
    admin = User(email="admin@AI.com", qualifications="the dude", expertise=4, password="admin_password")
    db.session.add(admin)

    df = pd.read_csv("classifier/static/birds.csv")
    db.session.bulk_insert_mappings(Bird, df.to_dict(orient="records"))
    db.session.commit()

# this are my new change
def init_db():
    app = create_app()
