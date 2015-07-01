# This file is for initializing Flask instance I think...

from flask import Flask # Basic Flask class

myapp = Flask(__name__) 
# myapp is an object of class Flask. __name__ is now __main__ ???

myapp.config.from_object('config')
# This is telling server to config as specified in config.py

from app import views
# This is importing views module (views.py we are gonna write)
# from app package, which is the app folder I think...

# Putting import at the bottom is to avoid circular references,
# because views.py will need to import myapp from here.