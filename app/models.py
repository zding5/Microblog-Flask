# This file is for defining database models

from app import db
# Import variable db from app package. (in __init__.py)

class User(db.Model):
	# Class User based on db.Model class ???
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	# Three fields of class User
	
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
