# This file is for defining database models
# SQLAlchemy is ORM (Object Relational Mapper) which associates python classes with tables, and instances of the classes with rows in tables.

from app import db
# Import variable db from app package. (in __init__.py)
from hashlib import md5
# For md5 encoding, for user avatar
from app import myapp

import sys

if sys.version_info >= (3, 0):
	enable_search = False
else:
	enable_search = True
	import flask.ext.whooshalchemy as whooshalchemy
# Since Python3 currently has problem with whooshalchemy, we disable full text search.

followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
# A relationship table for user's follower and followed. (A mapper)

class User(db.Model):
	# Class User based on db.Model, which is basically a declarative base class for ORM ...
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
	about_me = db.Column(db.String(140))
	# User's about me writing.
	last_seen = db.Column(db.DateTime)
	# Last seen time for this user.

	followed = db.relationship('User', secondary=followers, \
		primaryjoin=(followers.c.follower_id == id), \
		secondaryjoin=(followers.c.followed_id == id), \
		backref=db.backref('followers', lazy='dynamic'), \
		lazy='dynamic')
    
    # !!! ???
    # 'User' is the right side relation class (in this case it's the same as parent class, 'User')
    # secondary indicates the association table that is used for this relationship
    # primaryjoin indicates the condition for joining left table (follower users) to relationship table. 
    # secondaryjoin indicates the condition joining right table (followed users) to relationship table.
    # backref set followed attribute's back reference to be followers. (kind of like a reversed call ??? )
    # lazy argument indicates the execution mode for this query. A mode of dynamic sets up the query to not run until specifically requested.
    # ??? so it doesn't really query things ???


	def is_authenticated(self):
		# Return True unless the object represents a user that should not be allowed to authenticate for some reason.
		return True

	def is_active(self):
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

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)
		# Get an avatar image for user page.
		# The d=mm option returns the "mystery man" image, a gray silhouette of a person.
		# The s=N option requests the avatar scaled to the given size in pixels.

	@staticmethod
	def make_unique_nickname(nickname):
		if User.query.filter_by(nickname=nickname).first() is None:
			return nickname
		version = 2
		while True:
			new_nickname = nickname + str(version)
			if User.query.filter_by(nickname=new_nickname).first() is None:
				break
			version += 1
		return new_nickname
	# This is the User func for making unique nickname for solving duplicate nickname issue.
	# Say you have a nickname jeff, which is used, then the func would go through jeff1, jeff2 ... to find the first not used one and return.

	## Follower/Followed related
	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	# sqlalchemy provides simple append and remove for classes.

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count()>0
		# ??? 

	def followed_posts(self):
		return Post.query.join(followers, \
			(followers.c.followed_id == Post.user_id))\
		.filter(followers.c.follower_id == self.id)\
		.order_by(Post.timestamp.desc())
		# Join the post table and followers table with post's user_id as user being followed.
		# Filter out posts whose follower is this user.
		# Order them by newest to oldest.


class Post(db.Model):
	# Class Post. For posts.
	__searchable__ = ['body']
	# An array with all the database fields that will be in the searchable index.

	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	# user_id is a foreign key from User class.

	def __repr__(self):
		return '<Post %r>' % (self.body)

if enable_search:
	whooshalchemy.whoosh_index(myapp, Post)
# whooshalchemy index for searching ???







