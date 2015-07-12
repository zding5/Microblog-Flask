# This file is for defining database models

from app import db
# Import variable db from app package. (in __init__.py)

class User(db.Model):
	# Class User based on db.Model class ???
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	# Fields of class User
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	# Not a real field in the database diagram
	# For a one-to-many relationship a db.relationship field is normally defined on the "one" side.
	# 'Post': the 'many class'
	# backref, the field to be added to Post class to be called to refer back to User Class.
	# lazy ???

	def is_authenticated(self):
		# Return True unless the object represents a user that should not be allowed to authenticate for some reason.
		return True

	def is_activate(self):
		# Return True for users unless they are inactive (say banned)
		return True

	def is_anonymous(self):
		# Return True only for fake users that are not supposed to log in to the system
		return True 

	def get_id(self):
		try:
			return unicode(self.id) #python 2
		except NameError:
			return str(self.id) #python 3

	def __repr__(self):
		return '<User %r>' % (self.nickname)
	# Tells python how to print objects of class User

class Post(db.Model):
	# Class Post. For posts.
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	# user_id is a foreign key from User class.

	def __repr__(self):
		return '<Post %r>' % (self.body)
