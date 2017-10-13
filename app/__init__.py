
'''
Authors: Spencer Norris, Sabbir Rashid
File: app.py
Description: Implementation of server code for Wuu-Bernstein.

Note: you'll need to set the environment variable 'TWITTER_USER' to the
user of the local node.
'''

from datetime import datetime
from copy import copy
import requests
import pickle
import json
import time
import csv
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


#============ Globals, global population and local data read/write =============#

LOG = None
BLOCKED = None
USERS = None
ADDRESSES = None
TIME_MATRIX = None

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

def __READ_TIME_MATRIX():
    '''
    This matrix, implemented as a dict of dicts, defines what
    any given node knows about any other given node based on
    what their most recent known time stamp was.

    {
        'user_1': {
            'user_2': TIME
            ...
        }
        ...
    }

    If this matrix already exists as a pickled object, read
    it from the local disk. Otherwise, create a brand new 
    time matrix.
    '''

    def __unhash_dict():
        '''
        Reads in the hashed version of the dictionary.
        '''
        matrix = {}
        L = pickle.load(open("TIME_MATRIX.pickle", 'rb'))

        #Create dummy matrix
        for user in USERS:
            matrix[user] = {}
            for other_user in USERS:
                matrix[user][other_user] = 0

        #Populate new matrix
        for elem in L:
            user = elem[0]
            other_user = elem[1]
            t = elem[2]
            matrix[user][other_user] = t
        return matrix


    global USERS
    if not os.path.isfile('TIME_MATRIX.pickle'):
        matrix = {}
        if(USERS is not None) :
            for user in USERS:
                for other_user in USERS:
                    matrix[user][other_user] = 0
            return matrix
    else:
        return __unhash_dict()


def __BACKUP_MATRIX():
    '''
    Dictionaries in Python are not hashable,
    thus we need a small workaround for storing
    the pickled object when backing up the time matrix.
    '''
    global TIME_MATRIX
    L = []
    for user, v in TIME_MATRIX.items():
        for other_user, t in v.items():
            L.append((user,other_user,t))
    pickle.dump(L, open('TIME_MATRIX.pickle', 'wb'))



def __GET_BLOCKED_USERS():
    '''
    Returns a dictionary of what what users are 
    and aren't blocking other users.
    For example, if user_1 blocked user_2 at time 5,
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
    if(USERS is not None) :
        for user in USERS:
            blocked[user] = {}
            for other_user in USERS:
                if not other_user == user:
                    blocked[user][other_user] = UnblockEvent(user, other_user, 0)

    #Get all block and unblock events
    events = set(filter(
                lambda event: 
                type(event) is BlockEvent or type(event) is UnblockEvent, 
            LOG))

    #Set each user-user interaction to the most block or unblock
    for event in events:
        if event.time > blocked[event.user][event.target].time:
            blocked[event.user][event.target] = event

    return blocked
        


def __GET_ALL_USERS_ADDRESSES():
    '''
    Read in local two-column CSV file to get list of users and addresses.
    '''
    users = []
    addresses = []
    with open('users.csv', 'rb') as f:
        csv.reader(f)
        for row in reader:
            users.append(row[0])
            addresses.append(row[1])
    return users,addresses

def __GET_ALL_TWEETS():
    '''
    Returns list of all tweets currently in the log.
    '''
    global LOG
    return set(filter(lambda event: type(event) is Tweet, LOG))



#============================ Flask API Application ============================#

from flask import Flask
app = Flask(__name__)
#from app import views

#Populate globals on initialization
LOG = __READ_LOG_BACKUP()
USERS, ADDRESSES = __GET_ALL_USERS_ADDRESSES()
BLOCKED = __GET_BLOCKED_USERS()
TIME_MATRIX = __READ_TIME_MATRIX()
MY_USER = os.environ['TWITTER_USER']

@app.route("/tweet")
def tweet():
    time = datetime.utcnow()

    #Create tweet event, add to log

    #Prune log
    pruned_log = copy(LOG)

    #Send pruned log to all non-blocked users


    #Backup log, backup matrix
    __BACKUP_LOG()
    __BACKUP_MATRIX()
    return "Hello World!"



@app.route("/block")
def block():
    time = datetime.utcnow()

    #Find most recent block or unblock operation and remove it

    #Add this operation to log
    LOG.add(BlockEvent(MY_USER, target, time))

    #Update matrix
    TIME_MATRIX[MY_USER][MY_USER] = time

    #Backup log, matrix
    __BACKUP_LOG()
    __BACKUP_MATRIX()
    return "%s blocked at time %s" % (target, time)



@app.route("/unblock")
def unblock():
    time = datetime.utcnow()

    #Find most recent block or unblock operation and remove it

    #Add this operation to log

    #Update matrix

    #Backup log, matrix
    __BACKUP_LOG()
    __BACKUP_MATRIX()

    return "Hello World!"



@app.route("/view")
def view():
    '''
    Send ordered list of tweets as tuples to client.
    '''
    tweets = [(tweet.user, tweet.text, tweet.time) for tweet in __GET_ALL_TWEETS()]
    tweets = sort(tweets, key=lambda tweet: tweet[2], reverse=true)
    return json.dumps(tweets)
