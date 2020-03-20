import os
import json



# will need to repath when deployed
with open("config.json") as con_file:
    config = json.load(con_file)

class Config:
    SECRET_KEY = config.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = True
    MY_KEY = config.get("SECRET_KEY")
    FLICKR_API_KEY = config.get("FLICKR_API_KEY")
    EMAIL_ADMIN = config.get("EMAIL_ADMIN")
    EMAIL_PASS = config.get("EMAIL_PASS")
