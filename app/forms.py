# This file is for building/declaring a form class for login

from flask.ext.wtf import Form # Flask Form class
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form): 
	# Our LoginForm class is a subclass of Form, so we can use all the stuffs
	# provided by Flask-WTF.
	openid = StringField('openid', validators=[DataRequired()])
	# OpenIDs have the benefit that the authentication is done by the provider 
	# of the OpenID, so we don't have to validate passwords, which makes our 
	# site more secure to our users.
	remember_me = BooleanField('remember_me', default=False)

class EditForm(Form):
	# A class for user to enter about me.
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    # Now we handle duplicate nickname:

    # Overwrite constructor
    def __init__(self, original_nickname, *args, **kwargs):
    	# Take a new variale original_nickname (for new validate func to use).
    	Form.__init__(self, *args, **kwargs)
    	self.original_nickname = original_nickname

    # Overwrite validate()
    def validate(self):
    	if not Form.validate(self):
    		return False
    	# First pass the Form class validation ???

    	if self.nickname.data == self.original_nickname:
    		return True
    	# ???

    	user = User.query.filter_by(nickname=self.nickname.data).first()
    	if user != None:
    		self.nickname.errors.append('This nickname is already in use. Please choose another one.')
    		return False
    	return True

class PostForm(Form):
	post = StringField('post', validators=[DataRequired()])




