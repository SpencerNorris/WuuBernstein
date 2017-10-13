
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

def __UNHASH_DICT(f):
    '''
    Reads in the hashed versions of the TIME_MATRIX.
    '''
    matrix = {}
    L = pickle.load(f)

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


def __HASH_DICT(d):
    '''
    Writes out hashable versions of the TIME_MATRIX.
    '''
    L = []
    for user, v in d.items():
        for other_user, t in v.items():
            L.append((user,other_user,t))
    return L


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
    global USERS
    if not os.path.isfile('TIME_MATRIX.pickle'):
        matrix = {}
        for user in USERS:
            matrix[user] = {}
            for other_user in USERS:
                matrix[user][other_user] = 0
        return matrix
    else:
        return __UNHASH_DICT(open("TIME_MATRIX.pickle", 'rb'))


def __BACKUP_MATRIX():
    '''
    Dictionaries in Python are not hashable,
    thus we need a small workaround for storing
    the pickled object when backing up the time matrix.
    '''
    global TIME_MATRIX
    L = __HASH_DICT(TIME_MATRIX)
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
    with open('users.csv', 'r') as f:
        reader = csv.reader(f)
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


def __GET_PRUNED_LOG(other_user):
    '''
    Prunes the log so it only sends events after the most recent
    timestamp this node has on record for other_user.
    '''

    def __has_rec(event):
        '''
        Determines whether it's possible other_user knows about the event.
        '''
        global TIME_MATRIX
        return TIME_MATRIX[event.user][other_user] >= event.time

    global LOG
    pruned_log = copy(LOG)
    for event in LOG:
        if not __has_rec(event):
            pruned_log.add(event)
    return pruned_log


#============================ API Application ============================#


#Populate globals on initialization
LOG = __READ_LOG_BACKUP()
USERS, ADDRESSES = __GET_ALL_USERS_ADDRESSES()
BLOCKED = __GET_BLOCKED_USERS()
TIME_MATRIX = __READ_TIME_MATRIX()
MY_USER = os.environ['TWITTER_USER']
MY_CLIENT_ADDRESS = os.environ['CLIENT_ADDR']
VALID_COMMANDS = ['view', 'tweet', 'block', 'unblock']

def tweet(text):

    def __send_message(log, target_user):
        '''
        Carries out a transaction with the receiving node in order to transmit
        the pickled, hashed version of the time matrix and the pickled, hashed
        version of the log.
        '''
        global TIME_MATRIX
        global ADDRESSES

        #Retrieve target address
        target_addr = ADDRESSES[USERS.index(other_user)]

        #Create hashable objects, pickle them
        hashable_time_matrix = __HASH_DICT(TIME_MATRIX)
        L = list(log)
        hashable_time_matrix = pickle.dumps(hashable_time_matrix)
        L = pickle.dumps(L)

        #TODO: send pickled objects to mailbox of target user####################



    #Update time matrix
    global TIME_MATRIX
    global MY_USER
    time = datetime.utcnow()
    TIME_MATRIX[MY_USER][MY_USER] = time

    #Create tweet event, add to pruned logs
    tweet = Tweet(MY_USER, text, time)

    #Send pruned log, time matrix to all non-blocked users
    global USERS
    global ADDRESSES
    global BLOCKED
    for other_user in USERS:
        if not type(BLOCKED[MY_USER][other_user]) is BlockEvent:
            pruned_log = __GET_PRUNED_LOG(other_user)
            pruned_log.add(tweet)
            __transmit_log(pruned_log,other_user)

    #Backup log, backup matrix
    LOG.add(tweet)
    __BACKUP_LOG()
    __BACKUP_MATRIX()



def block(user):
    '''
    Add block event to local log for target user.
    '''
    global LOG
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



def unblock(target):
    global LOG
    global MY_USER
    time = datetime.utcnow()
    event = UnblockEvent(MY_USER, target, time)

    #Find most recent block or unblock operation and remove it
    

    #Add this operation to log

    #Update matrix

    #Backup log, matrix
    __BACKUP_LOG()
    __BACKUP_MATRIX()

    return "Hello World!"



def view():
    '''
    Send ordered list of tweets as tuples to client.
    '''
    global MY_CLIENT_ADDRESS

    #Pull in all tweets and sort
    tweets = [(tweet.user, tweet.text, tweet.time) for tweet in __GET_ALL_TWEETS()]
    tweets = sort(tweets, key=lambda tweet: tweet[2], reverse=true)

    #filter out tweets this user isn't allowed to see

    #Send tweets back to client
    return json.dumps(tweets)



def receive_tweet(other_log, other_time_matrix):
    '''
    Reads in log, time matrix from other node and updates each.
    '''
    
    #Update local time matrix

    #Update local event log, including updating block and unblock states

    #Backup
    __BACKUP_LOG()
    __BACKUP_MATRIX()



def get_message():
    '''
    Retrieves a message from the mailbox daemon.
    '''
    pass


#MAIN LOOP
while(1):
    cmd = get_message() #Retrieves message of form ('command', [Args])

    #No messages right now
    if cmd is None:
        continue

    #Catch invalid commands
    if not cmd[0] in VALID_COMMANDS:
        print("Invalid command!")
        continue

    #Handle commands
    #NOTE: Can always assume commands come from client
    if cmd[0] == 'block':
        block(cmd[1])
    elif cmd[0] == 'unblock':
        unblock(cmd[1])
    elif cmd[0] == 'tweet':
        tweet(cmd[1])
    elif cmd[0] == 'view':
        view()

    #Otherwise, we're receiving a tweet from another node
    else:
        other_log = set(pickle.loads(cmd[1][0]))
        other_time_matrix = __UNHASH_DICT(pickle.loads(cmd[1][1]))
        receive_tweet(set(other_log), other_time_matrix)
