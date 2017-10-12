
'''
Authors: Spencer Norris, Sabbir Rashid
File: app.py
Description: Implementation of server code for Wuu-Bernstein.
'''

from datetime import datetime
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
	'''
	Returns a dictionary of what what users are and aren't blocking other users.
	ex.
	{
		'user_1' : {
			'user_2' : BlockEvent('user_1', 'user_2', 5)
		}
		...
	}

	meaning user_1 blocked user_2 at time 5. If user_1 unblocks user_2 at time 6,

	{
		'user_1' : {
			'user_2' : UnblockEvent('user_1', 'user_2', 6)
		}
		...
	}
	'''
	global LOG
	global USERS

	#Create dictionary of users pointing to dictionary of other users
	#Pointing to the earliest possible state between users of the system
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

def __GET_ALL_TWEETS():
	'''
	Returns list of all tweets currently in the log
	'''
	global LOG
	return set(filter(lambda event: type(event) is Tweet, LOG))


LOG = __READ_LOG_BACKUP()
BLOCKED = __GET_BLOCKED_USERS()
USERS = __GET_ALL_USERS()


#============================ Flask API Application ============================#

from flask import Flask
app = Flask(__name__)
#from app import views

@app.route("/tweet")
def tweet():
	time = datetime.utcnow()

	#Create tweet event, add to log

	#Send log to all non-blocked users

	__BACKUP_LOG()
	return "Hello World!"

@app.route("/block")
def block():
	time = datetime.utcnow()
	#Find most recent block or unblock operation and remove it

	#Add this operation to log


	__BACKUP_LOG()
	return "%s blocked at time %s" % (target, time)

@app.route("/unblock")
def unblock():
	time = datetime.utcnow()

	#Find most recent block or unblock operation and remove it

	#Add this operation to log

	#Backup log

	return "Hello World!"

@app.route("/show")
def show():
	#Return ordered list of all tweets
	return "Hello World!"