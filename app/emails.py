from flask.ext.mail import Message
# For building and sending email message.
from app import mail

from flask import render_template
from config import ADMINS

from app import myapp

from .decorators import async

@async
# from decorators.py
# The decorator we write ourselves !!! It handles asynchronous requests for all places we want async requests.
def send_async_email(myapp, msg):
	with myapp.app_context():
	# ???
		mail.send(msg)

# Instead of multithreading, we can also use multiprocessing.
# Then we would use Pool class from multiprocessing module ... ...


def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	send_async_email(myapp, msg)
# Instead of just "mail.send(msg)", we let send_async_email send an asynchronous request.

def follower_notification(followed, follower):
	print followed

	send_email("[microblog] %s is now following you!" % follower.nickname,
				ADMINS[0],
				[followed.email],
				render_template("follower_email.txt", 
                               user=followed, follower=follower),
				render_template("follower_email.html", 
                               user=followed, follower=follower))
# Like the HTML from our views, the bodies of email messages are an ideal candidate for using templates !!!




















