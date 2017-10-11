
'''
Authors: Spencer Norris, Sabbir Rashid
File: app.py
Description: Implementation of server code for Wuu-Bernstein.
'''


#Set up globals, populate with pre-existing data
BLOCKED = set()
TWEETS = set()
USERS = set()

#=========== Flask Application ===========#
from flask import Flask

app = Flask(__name__)
from app import views

@app.route("/tweet")
def tweet():
	return "Hello World!"

@app.route("/block")
def block():
	return "Hello World!"

@app.route("/unblock")
def unblock():
	return "Hello World!"

@app.route("/show")
def show():
	return "Hello World!"