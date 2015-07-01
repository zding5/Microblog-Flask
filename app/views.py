# This file contains view module, which is a handler that respond to requests 
# from web browsers or other clients. 

# So, yeah, basically, the handler.

from app import myapp
# I don't know why you can just find myapp in app package...???
from flask import render_template
# This is for render Jinja templates
from flask import flash, redirect 
# ...
from .forms import LoginForm 
# This if for loginform

@myapp.route('/')
@myapp.route('/index')
def index():
	user = {'nickname': 'Miguel'} # Some fake user
	posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
	return render_template('index.html', title='Home', user=user, post=post)
	# Render Jinja template with parameters.

# Now let's handle login form!
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    # Create a loginform I think...
    return render_template('login.html', title='Sign In', form=form)
