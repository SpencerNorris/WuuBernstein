
'''
Authors: Spencer Norris, Sabbir Rashid
File: app.py
Description: Implementation of server code for Wuu-Bernstein.
'''

import requests
import pickle
import time
import os

#============== Globals, global population and data modification ===============#
LOG = __READ_LOG_BACKUP()
BLOCKED = set()
USERS = set()


def __BACKUP_LOG():
	global LOG
	L = list(LOG)
	pickle.dump(L, open('LOG.pickle', 'wb'))


def __READ_LOG_BACKUP():
	'''
	Read our pickled copy of the log between restarts.
	If the file doesn't exist, return empty log.
	'''
	if not os.path.isfile('LOG.pickle'):
		return set()
	else:
		L = pickle.load(open("LOG.pickle,", 'rb'))
		return set(L)


def __GET_BLOCKED_USERS():
	global LOG
	pass


def __GET_ALL_USERS():
	global LOG
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