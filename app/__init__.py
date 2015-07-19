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
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
# These are all for mailing (reporting) from config.py
from flask.ext.mail import Mail

from .momentjs import momentjs

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

mail = Mail(myapp)
# Mail service object

myapp.jinja_env.globals['momentjs'] = momentjs
# Tells Jinja2 to expose momentjs class as a global var to all templates.

# Enabling reporting via email.
if not myapp.debug:
# Meaning we are in production mode
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    myapp.logger.addHandler(mail_handler)
# We are only enabling the emails when we run without debugging.
# use "python -m smtpd -n -c DebuggingServer localhost:25" to run a fake email server.

# Enabling logging (for events and bugs)
if not myapp.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    # Limiting the log to be 1MB.

    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    # Formatting log.

    myapp.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    myapp.logger.addHandler(file_handler)
    myapp.logger.info('microblog startup')


from app import views
# This is importing views module (views.py we are gonna write)
# from app package, which is the app folder I think...

from app import models
# This is importing models module (models.py)
# This is for database models

# Putting import at the bottom is to avoid circular references,
# because views.py will need to import myapp from here.