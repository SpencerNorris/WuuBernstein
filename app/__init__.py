
'''
Authors: Spencer Norris, Sabbir Rashid
File: app.py
Description: Implementation of server code for Wuu-Bernstein.
'''


#Set up globals, populate with pre-existing data
BLOCKED = set()
TWEETS = set()

#=========== Flask Application ===========#
from flask import Flask

app = Flask(__name__)
from app import views

@app.route("/")
def hello():
    return "Hello World!"