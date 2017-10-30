#!/usr/bin/env python3
'''
Authors: Spencer Norris, Sabbir Rashid
Description: Script for Wuu-Bernstein client.
'''
from datetime import datetime
from ast import literal_eval as make_tuple
import sys
import socket 
import time
import os
import calendar

MY_USER = os.environ['TWITTER_USER']

def client(client_port,hostname):
    #hostname = "127.0.0.1"
    mb_port=9000
    #client_port=9999
    mb_address=(hostname,mb_port)
    client_addr = (hostname,int(client_port))
    
    blocked_list = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(client_addr)
    print "Client ", sock.getsockname(), " created"
    sock.connect(mb_address)

    def __tweet(message) :
        print "Tweeting..."
        #sock.send(message)
        #print "Response: ", sock.recv(1024)
        sock.send("0")
        response = None
        while response is None :
            print "Waiting for first response..."
            response = sock.recv(1024).decode().strip()
            print "Received response:",response
            if response == 'Ack' :
                print "Received first Acknowledgement"
                sock.send(str(sys.getsizeof(message)))
                #sock.send('1024')
                print "Sent buffer size"
                response2 = None
                while response2 is None :
                    print "Waiting for second response..."
                    response2 = sock.recv(1024).decode()
                    print "Received response:",response2
                    if response2 == 'Ack' :
                        print "Received second Acknowledgement, sending tweet"
                        sock.send(message)
                        response3 = None
                        while response3 is None :
                            print "Waiting for third response..."
                            response3 = sock.recv(1024).decode()
                            print "Received response:",response3
                            if response3 == 'Ack' :
                                print "Received third Acknowledgement, sending time"
                                etime = int(time.time())#datetime.utcnow()
                                sock.send(str(etime))
                                response4 = None
                                while response4 is None :
                                    print "Waiting for fourth response..."
                                    response4 = sock.recv(1024).decode()
                                    print "Received response:",response4
                                    if response4 == 'Ack' :
                                        print "Received fourth Acknowledgement, sending user"
                                        sock.send(MY_USER)

        #sock.close()
        #print message
        #pass

    def __view(message) :
        print "Showing..."
        sock.send("1")
        response = None
        while response is None :
            print "Waiting for view response..."
            response = sock.recv(1024).decode()
            print "Received response:",response
            if response == 'Ack' :
                print "Received view Acknowledgement"
                sock.send("Ack")
                response2 = None
                while response2 is None :
                    response2 = sock.recv(1024).decode()
                    print "Received response:",response
                    if response2 == 'Ack' :
                        print "Received second Acknowledgement"
                        sock.send("Ack")
                        response3 = None
                        print "Waiting for queue size..."
                        response3 = sock.recv(1024).decode()
                        print "Received response:",response3
                        queuesize=int(response3)
                        sock.send("Ack")
                        for i in range(0,queuesize) :
                            msg = sock.recv(1024).decode()
                            if make_tuple(msg)[0] not in blocked_list and int(make_tuple(msg)[1]) < int(time.time()):
                                print "Received message:", msg
                            sock.send("Ack")
#        entry=sock.recv(buffer_size)
#        print entry.decode()

    def __block(message):
        print "Blocking..."
        sock.send("2")
        response = None
        while response is None :
            print "Waiting for first response..."
            response = sock.recv(1024).decode().strip()
            print "Received response:",response
            if response == 'Ack' :
                print "Received first Acknowledgement"
                sock.send(str(sys.getsizeof(message)))
                #sock.send('1024')
                print "Sent buffer size"
                response2 = None
                while response2 is None :
                    print "Waiting for second response..."
                    response2 = sock.recv(1024).decode()
                    print "Received response:",response2
                    if response2 == 'Ack' :
                        print "Received second Acknowledgement, sending block"
                        sock.send(message)
                        response3 = None
                        while response3 is None :
                            print "Waiting for third response..."
                            response3 = sock.recv(1024).decode()
                            print "Received response:",response3
                            if response3 == 'Ack' :
                                print "Received third Acknowledgement, sending time"
                                etime = int(time.time())
                                sock.send(str(etime))
                                response4 = None
                                while response4 is None :
                                    print "Waiting for fourth response..."
                                    response4 = sock.recv(1024).decode()
                                    print "Received response:",response4
                                    if response4 == 'Ack' :
                                        print "Received fourth Acknowledgement, sending user"
                                        sock.send(MY_USER)
                                        print "Adding user to Blocked List"
                                        blocked_list.append(message)

        #pass

    def __unblock(message):
        print "Unblocking..."
        sock.send("0")
        response = None
        while response is None :
            print "Waiting for first response..."
            response = sock.recv(1024).decode().strip()
            print "Received response:",response
            if response == 'Ack' :
                print "Received first Acknowledgement"
                sock.send(str(sys.getsizeof(message)))
                #sock.send('1024')
                print "Sent buffer size"
                response2 = None
                while response2 is None :
                    print "Waiting for second response..."
                    response2 = sock.recv(1024).decode()
                    print "Received response:",response2
                    if response2 == 'Ack' :
                        print "Received second Acknowledgement, sending unblock"
                        sock.send(message)
                        response3 = None
                        while response3 is None :
                            print "Waiting for third response..."
                            response3 = sock.recv(1024).decode()
                            print "Received response:",response3
                            if response3 == 'Ack' :
                                print "Received third Acknowledgement, sending time"
                                etime = int(time.time())
                                sock.send(str(etime))
                                response4 = None
                                while response4 is None :
                                    print "Waiting for fourth response..."
                                    response4 = sock.recv(1024).decode()
                                    print "Received response:",response4
                                    if response4 == 'Ack' :
                                        print "Received fourth Acknowledgement, sending user"
                                        sock.send(MY_USER)
                                        try :
                                            print "Removing user from Blocked List"
                                            blocked_list.remove(message)
                                        except : 
                                            print "User not in blocked list"
        #pass
    
    command = {
                'tweet': __tweet,
                'view': __view,
                'block': __block,
                'unblock': __unblock,
            }

    VALID_COMMANDS = ['view', 'tweet', 'block', 'unblock', 'exit']
    while True :
        input_var = raw_input("Enter a command: ")
        endIndex=-1
        input_command = ""
        for i in range(len(input_var)) :
            if input_var[i] is ' ' :
                endIndex = i
                break
        if endIndex !=-1 :
            input_command = input_var[0:endIndex]
        else :
            input_command = input_var
        if not input_command.lower() in VALID_COMMANDS:
            print("Invalid command: " + input_command.lower() + "\n")
            continue
        elif input_command.lower() == 'exit':
            break
        else:
            if endIndex !=-1 :
                command[input_command.lower()](input_var[endIndex+1:])
            else : 
                command[input_command.lower()](input_var)
        #return 0
    

if __name__ == '__main__':
    #app.run()
    client(sys.argv[1],sys.argv[2])
    #sys.exit(client())
