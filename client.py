#!/usr/bin/env python3
'''
Authors: Spencer Norris, Sabbir Rashid
Description: Script for Wuu-Bernstein client.
'''

import sys
import socket 


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    hostname = "127.0.0.1"
    mb_port=9000
    h_port=9999
    mb_address="127.0.0.1:9000"

    def __tweet(message) :
        print "Tweeting..."
        #sock.connect(hostname + ":" + mb_port)
        sock.connect(mb_address)
        sock.send("0")
        response = sock.recv(40)
        if response.decode() == "Ack" :
            sock.send(sys.getsizeof(message))
            response2 = sock.recv(40)
            if response2.decode() == "Ack" :
                sock.send(message)

        close(sock)
        #print message
        #pass

    def __view() :
        print "Showing..."
        #sock.connect(hostname,mb_port)
        sock.connect(mb_address)
        sock.send("1")
        response = sock.recv(1024)
        buffer_size = atoi(response.decode())
        sock.send("Ack")
        entry=sock.recv(buffer_size)
        print entry.decode()

    def __block(message):
        print "Blocking..."
        #sock.connect(hostname,mb_port)
        sock.connect(mb_address)
        sock.send("2")
        response = sock.recv(40)
        if response.decode() == "Ack" :
            sock.send(sys.getsizeof(message))
            response2 = sock.recv(40)
            if response2.decode() == "Ack" :
                sock.send(message)
        print message
        #pass

    def __unblock(message):
        print "Unblocking..."
        #sock.connect(hostname,mb_port)
        sock.connect(mb_address)
        sock.send("3")
        response = sock.recv(40)
        if response.decode() == "Ack" :
            sock.send(sys.getsizeof(message))
            response2 = sock.recv(40)
            if response2.decode() == "Ack" :
                sock.send(message)
        print message
        #pass
    
    command = {
                'tweet': __tweet,
                'view': __view,
                'block': __block,
                'unblock': __unblock,
            }

    VALID_COMMANDS = ['view', 'tweet', 'block', 'unblock', 'exit']
    while(1):
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
        return 0
    

if __name__ == '__main__':
    #app.run()
    sys.exit(client())
