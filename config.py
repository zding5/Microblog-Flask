# This file is for configurations

# When you use this in a new environment, the config
# will adapt to the new environment, so you don't
# have to change codes.

# Now, configuring for Flask-WTF (Handling web forms)
WTF_CSRF_ENABLED = True # Prevending CSRF
SECRET_KEY = 'ok-this-is-not-what-i-have-in-mind' # Private key??? for CSRF prevention

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
# This are just openid providers for our login

import os
basedir = os.path.abspath(os.path.dirname(__file__))
# This is the base directory, set to this file's directory

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# Path of our database file
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# Folder for our migrate data files

## mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None
# administrator list
ADMINS = ['you@example.com']
## These two are for reporting mechanism, say reporting bug via email.

# Pagination
POSTS_PER_PAGE = 3










