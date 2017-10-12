
'''
Authors: Spencer Norris, Sabbir Rashid
File: app.py
Description: Implementation of server code for Wuu-Bernstein.
'''

import requests
import pickle
import time
import os

#========================== Class Structure ====================================#

class Tweet:
	def __init__(self, user, text, time):
		self.user = user
		self.text = text
		self.time = time


class BlockEvent:
	def __init__(self, user, target, time):
		self.user = user
		self.target = target
		self.time = time


class UnblockEvent:
	def __init__(self, user, target, time):
		self.user = user
		self.target = target
		self.time = time


#============== Globals, global population and data modification ===============#

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
	global USERS

	#Create dictionary of users pointing to dictionary of other users
	#Pointing to most recent block or unblock event
	blocked = {}
	for user in USERS:
		blocked[user] = {}
		for other_user in USERS:
			if not other_user == user:
				blocked[user][other_user] = UnblockEvent(user, other_user, 0)

	#Get all block and unblock events
	events = set(filter(
					lambda event: type(event) is BlockEvent or type(event) is UnblockEvent, 
				  LOG))

	#Set each user-user interaction to the most block or unblock
	for event in events:
		if event.time > blocked[event.user][event.target].time:
			blocked[event.user][event.target] = event

	return blocked
		


def __GET_ALL_USERS():
	'''
	Read in local file to get list of users and addresses
	'''
	pass


LOG = __READ_LOG_BACKUP()
BLOCKED = set()
USERS = set()


#============================== Flask Application =============================#

from flask import Flask
app = Flask(__name__)
#from app import views

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