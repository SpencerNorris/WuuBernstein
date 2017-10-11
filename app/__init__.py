
'''
Authors: Spencer Norris, Sabbir Rashid
File: app.py
Description: Implementation of server code for Wuu-Bernstein.
'''

import requests
import pickle
import time

#============== Globals, global population and data modification ===============#
BLOCKED = set()
USERS = set()
LOG = set()


def __BACKUP_LOG():
	def __log_to_list():
		'''
		Sets aren't hashable, so convert to a list.
		'''
		pass
	pass


def __READ_LOG_BACKUP():
	def __list_to_log():
		'''
		Get a set from the hashed list.
		'''
		pass
	pass


def __GET_BLOCKED_USERS():
	pass


def __GET_ALL_USERS():
	pass


#============================== Flask Application =============================#
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