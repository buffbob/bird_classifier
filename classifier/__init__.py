from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from classifier.config import Config

app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login_page"

def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from classifier.admin.routes import admin
    from classifier.users.routes import users
    from classifier.main.routes import main
    from classifier.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    return app
