import os
from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel
from flask import request

#Where all libraries are initialised to a variable to be exported, according to MVT style of architecture.
app = Flask(__name__)

app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
moment = Moment(app)


babel= Babel(app)










from app import routes, models, errors