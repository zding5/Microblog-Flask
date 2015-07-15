# This file is for initializing Flask instance I think...

from flask import Flask # Basic Flask class
from flask.ext.sqlalchemy import SQLAlchemy # Our database

import os
from flask.ext.login import LoginManager
# Handling user login
from flask.ext.openid import OpenID
# For OpenID
from config import basedir
# import base directory from config.py


myapp = Flask(__name__) 
# myapp is an object of class Flask. __name__ is now __main__ ???

myapp.config.from_object('config')
# This is telling server to config as specified in config.py

db = SQLAlchemy(myapp)
# Create our database object
# sqlalchemy api object is a big wrap of db basics I think ... ??? Including engine, session and etc.

lm = LoginManager()
# User Login handler
lm.init_app(myapp)
lm.login_view = 'login' 
# Name of the login_view for ... ???

oid = OpenID(myapp, os.path.join(basedir, 'tmp'))
# The Flask-OpenID extension requires a path to a temp folder where files can be stored.

from app import views
# This is importing views module (views.py we are gonna write)
# from app package, which is the app folder I think...

from app import models
# This is importing models module (models.py)
# This is for database models

# Putting import at the bottom is to avoid circular references,
# because views.py will need to import myapp from here.