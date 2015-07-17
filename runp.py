#!flask/bin/python

# This file is for production run (with the debug mode off so you can publish)

from app import myapp
myapp.run(debug=False)
