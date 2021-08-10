from flask import Flask
from flask_login import LoginManager
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

# Forms
app.config['SECRET_KEY'] = "key_for_doctor_project"

# SQL
basedir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Facebook
app.config['FACEBOOK_OAUTH_CLIENT_ID'] = os.environ.get('app_id')
app.config['FACEBOOK_OAUTH_CLIENT_SECRET'] = os.environ.get('secret_key')

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Setup SQL
db = SQLAlchemy(app)
Migrate(app, db)
