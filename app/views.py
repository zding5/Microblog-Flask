# This file contains view module, which is a handler that respond to requests 
# from web browsers or other clients. 

# So, yeah, basically, the handler.

from app import myapp
# I don't know why you can just find myapp in app package...???
from app import db, lm, oid
# Import db object, login manager object and open id from app

from flask import render_template
# This is for render Jinja templates
from flask import flash 
# This is for showing quick message
from flask import redirect
# This is to redirect window to another page
from flask.ext.login import login_user, logout_user, current_user, login_required
# Import a bunch of login related params form flask login

from .forms import LoginForm 
# This is the class for loginform
from .models import User
# Import User class from models.py

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
	return render_template('index.html', title='Home', user=user, post=posts)
	# Render Jinja template with parameters.

# Now let's handle login form!
@myapp.route('/login', methods=['GET', 'POST'])
# Tell Flask that only GET or POST are accepted
@oid.loginhandler # ???
def login():
    form = LoginForm() 
    # Create a loginform I think...
    if form.validate_on_submit():
        # Built in validation func from LoginForm
        # class
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        # flash() is to show quick message on the 
        # NEXT page presented to the user.
        return redirect('/index')
        # This is called before our users even see the
        # form, so it will return False the first time.
        # And so we render the login form.

        # But later when form is submitted, this returns
        # True, and we redirect user to their homepage.

    return render_template('login.html',
                            title='Sign In',
                            form=form,
                            providers=app.config['OPENID_PROVIDERS']
                            # getting openid providers form config.py
                            )

@lm.user_loader
# This callback is used to reload the user object from the user ID stored in the session.
def load_user(id):
    return User.query.get(int(id))
    # Convert id from unicode to int for lm.user_loader only takes in int.





