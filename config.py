# _*_ coding: utf-8 _*_
## This is for unicode support !!!

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
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465

# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# Get these from environment vars.
# Have to set these if on server ???

MAIL_USERNAME = "myblog.ziqiao.ding"
MAIL_PASSWORD = "abc123456cba"

MAIL_USE_TLS = False
MAIL_USE_SSL = True

# administrator list
ADMINS = ['myblog.ziqiao.ding@gmail.com']
# Admin email for this site.


# Pagination
POSTS_PER_PAGE = 3

# For full text search
WHOOSE_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50

# For language supports
LANGUAGES = {
	'en': 'English',
	'es': 'Español',
	'zh': '中文'
}

BABEL_DEFAULT_LOCALE = 'zh_CN'

# Supporing ñ because we specified '# _*_ coding: utf-8 _*_' on the top !!!






