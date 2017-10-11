#!/usr/bin/env python3
'''
Authors: Spencer Norris, Sabbir Rashid
File: node.py
Description: Root process for Wuu-Bernstein implementation.
	Sets up a client process that a user can attach to and
	a server process that handles incoming requests.
'''


def client():
	pass


def app():
	pass


def main():
   manager = Manager()
   d = manager.dict()
   app_p = Process(target=app)
   client_p = Process(target=client, args=(d))
   app_p.start()
   client_p.start()
