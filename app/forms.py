# This file is for building/declaring a form class for login

from flask.ext.wtf import Form # Flask Form class
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form): 
	# Our LoginForm class is a subclass of Form, so we can use all the stuffs
	# provided by Flask-WTF.
	openid = StringField('openid', validators=[DataRequired()])
	# OpenIDs have the benefit that the authentication is done by the provider 
	# of the OpenID, so we don't have to validate passwords, which makes our 
	# site more secure to our users.
	remember_me = BooleanField('remember_me', default=False)

