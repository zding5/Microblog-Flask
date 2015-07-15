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
from flask import session
# Flask request session I think ...
from flask import g
# Flask globals
from flask import url_for, request # request ???
from flask.ext.login import login_user, logout_user, current_user, login_required
# Import a bunch of login related params form flask login

from .forms import LoginForm 
# This is the class for loginform
from .models import User
# Import User class from models.py

@myapp.route('/')
@myapp.route('/index')
@login_required # Insure this page is only viewable by logged in users.
def index():
    user = g.user # Set by before_request() I think ...
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
@lm.user_loader
# This callback is used to reload the user object from the user ID stored in the session.
def load_user(id):
    return User.query.get(int(id))
    # query() is inherited from db.Model Class I think ...
    # Convert id from unicode to int for lm.user_loader only takes in int.

@myapp.before_request
# Any functions that are decorated with before_request will run before the view function each time a request is received.
def before_request():
    g.user = current_user
    # current_user global is set by Flask-Login.

@myapp.route('/login', methods=['GET', 'POST'])
# Tell Flask that only GET or POST are accepted
@oid.loginhandler # Tells flask that this func is our login view func
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index')) # url_for is better way than just giving the plain url
    # The idea here is that if there is a logged in user already we will not do a second login on top.
    # The g global is setup by Flask as a place to store and share data during the life of a request. ???
    # And we will use g to store logged in users.

    form = LoginForm() 
    # Create a loginform I think...
    if form.validate_on_submit():
        # Built in validation func from LoginForm class
        session['remember_me'] = form.remember_me.data
        # This is a flask session (not to be confused with db.session)
        # Data stored in the session object will be available during that request and any future requests made by the same client
        # until explicitly removed.

        # We have one session container for each client. 
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])

    return render_template('login.html',
                            title='Sign In',
                            form=form,
                            providers=myapp.config['OPENID_PROVIDERS']
                            # getting openid providers form config.py
                            )


@oid.after_login
def after_login(resp):
    # resp contains information returned by the OpenID provider.
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    # Validation

    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    # Create new user if it doesn't exist.

    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    # Load 'remember_me' value from session.
        
    login_user(user, remember=remember_me)
    # Register user as a valid login using login_user.
    return redirect(request.args.get('next') or url_for('index'))

@myapp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))










