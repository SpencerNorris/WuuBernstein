#!/usr/bin/env python3
'''
Authors: Spencer Norris, Sabbir Rashid
Description: Script for Wuu-Bernstein client.
'''

import sys
import socket 


def client():
    hostname = "127.0.0.1"
    mb_port=9000
    client_port=9999
    mb_address=(hostname,mb_port)
    client_addr = (hostname,client_port)
    
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

        #sock.close()
        #print message
        #pass

    def __view() :
        print "Showing..."
        #sock.connect(mb_address)
        sock.send("1")
        response = sock.recv(1024)
        buffer_size = atoi(response.decode())
        sock.send("Ack")
        entry=sock.recv(buffer_size)
        print entry.decode()

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
    client()
    #sys.exit(client())
