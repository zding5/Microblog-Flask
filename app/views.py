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
# This is the class for loginform from form.py
from .models import User
# Import User class from models.py
from forms import EditForm
# This is the class for Editform from form.py
from forms import PostForm
from models import Post
# These are for submitting posts.

from datetime import datetime
# datetime datatype

from config import POSTS_PER_PAGE

from forms import SearchForm

from config import MAX_SEARCH_RESULTS

from .emails import follower_notification
# import follower_notification from emails.py

from app import babel
from config import LANGUAGES
# lang supports

from flask.ext.babel import gettext
# This is for translating strings for different langs
# We need to use gettext() to mark out all texts we want to be translated, or use _() as a shorter alias. Why ??? 

@myapp.route('/', methods=['GET', 'POST'])
@myapp.route('/index', methods=['GET', 'POST'])

@myapp.route('/index/<int:page>', methods=['GET', 'POST'])
# For routing to different pages.

@login_required # Insure this page is only viewable by logged in users.
def index(page=1):# page by default is set to 1.

    form = PostForm()
    # A postform object for submitting posts.
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash(gettext('Your post is now live!'))
        return redirect(url_for('index'))
        # Force redirct instead of just let it go to render the same index page.
        # This is for when user refresh the page.
        # Refresh submits the last request, so if we don't for redirect, when refreshing, it will submit the same form again !!!

    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    # get posts from db.
    # The paginate method can be called on any query object. It takes three arguments:
    # page number, number of items per page, error flag.

    return render_template('index.html', title='Home', form=form, posts=posts)
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
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
    # For supporting last seen data functionality
        
        g.search_form = SearchForm()
        # Make search form global, available for all pages.

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
        flash(gettext('Invalid login. Please try again.'))
        return redirect(url_for('login'))
    # Validation

    user = User.query.filter_by(email=resp.email).first()
    if user is None:
    # Create new user if it doesn't exist.
        # flash('Good, a user!') #
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        # This is for solving duplicate nickname issue !!!
        # We now let user pick a unique nickname.
        # Do we still want the part before ???

        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()

        db.session.add(user.follow(user))
        db.session.commit()
        # Make user its own follower. This is for displaying user's own posts when displaying all followed post.
        # ... Might not be neccesary for us.

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


@myapp.route('/user/<nickname>')
@myapp.route('/user/<nickname>/<int:page>')
@login_required
# For certain user personal page.
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash(gettext('User %(nickname)s not found.', nickname=nickname)) ### right ???
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html', user=user, posts=posts)


@myapp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
# For user editing about me
    form = EditForm(g.user.nickname)
    # The overwritten constructor takes in original nickname.
    
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash(gettext('Your changes have been saved.'))
        return redirect(url_for('edit'))
    else:
    # When would validate fail ???
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


## Error handling
@myapp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@myapp.errorhandler(500)
def not_found_error(error):
    db.session.rollback()
    # If the exception was triggered by a database error then the database session is going to arrive in an invalid state, so we have to roll it back in case a working session is needed for the rendering of the template for the 500 error.
    return render_template('500.html'), 500


@myapp.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user is None:
        flash(gettext('User %(nickname)s not found.', nickname=nickname))
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t follow yourself!'))
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash(gettext('Cannot follow ' + '%(nickname)s',nickname=nickname + '.'))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You are now following ' + '%(nickname)s',nickname=nickname + '!' ))
    follower_notification(user, g.user) # from emails.py
    return redirect(url_for('user', nickname=nickname))


@myapp.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(gettext('User %(nickname)s not found.', nickname=nickname))
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t unfollow yourself!'))
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash(gettext('Cannot unfollow' + '%(nickname)s', nickname=nickname + '.'))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You have stopped following ' + '%(nickname)s',nickname=nickname + '.'))
    return redirect(url_for('user', nickname=nickname))


@myapp.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))
# Just collects the search query from the form and then redirects to another page passing this query as an argument.
# The reason the search work isn't done directly here is that if a user then hits the refresh button the browser will put up a warning indicating that form data will be resubmitted.

@myapp.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html', query=query, results=results)


@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(LANGUAGES.keys())
    # ???
    print "here?"
    return 'zh_CN'




