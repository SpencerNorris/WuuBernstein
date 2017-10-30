'''
Authors: Spencer Norris, Sabbir Rashid
File: mailbox.py
Description: mailbox for handling message reception from remote processes.
'''
from datetime import datetime
from copy import copy
import requests
import pickle
import time
import socket
import sys
import threading
import Queue

class Mailbox:
    def __init__(self):
        self.host_ip = '127.0.0.1'
        self.mail_port = 9000
        self.client_port = 9999
        self.server_port = 5000
        self.mailbox = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mailbox.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mailbox.bind((self.host_ip, self.mail_port))
        self.msgQ = Queue.PriorityQueue()
        self.threads = []
        
        self.VALID_TYPES = ['0', '1', '2', '3', '4']

    def __handle_req(self,client_sock, addr):

        '''
        Implementation of handshakes for receiving 'show' requests from client,
        receiving 'tweet' requests from other nodes,
        and sending 'show' and 'tweet' requests to server.
        '''

        def __listen(self,client_sock, addr) :
            buffer_size=1024
            print "Listening to Client ",addr #client_sock.getsockname()
            while True :
                try :
                    input_data = client_sock.recv(buffer_size).decode()
                    if input_data :
                        if not input_data in self.VALID_TYPES :
                            print "Invalid message type"
                        else :
                            print "Valid message type"
                            #command(input_data)
                            if input_data == '0' :
                            #    __handle_tweet(self)
                                print "Sending Tweet Acknowledgement to",addr
                                client_sock.send('Ack')
                                response = None
                                while response is None :
                                    print "Waiting for response from",addr
                                    response = client_sock.recv(1024).decode()
                                    print "Received response:",response
                                    buffer_size = int(response)
                                print "Sending Tweet Buffer Size Acknowledgement to",addr
                                client_sock.send('Ack')
                                entry = None
                                while entry is None :
                                    entry=client_sock.recv(buffer_size).decode()
                                    print "Received Tweet:", entry.decode()
                                #msgCount += 1
                                time = datetime.utcnow()
                                self.msgQ.put((time,0,entry))# add tweet to message queue
                                #self.msgQ.put((time,entry))# add tweet to message queue
                            elif input_data == '1' :
                                print "Received View Request from ",addr
                                print "Sending View Acknowledgement to",addr
                                client_sock.send('Ack')
                                response = None
                                while response is None :
                                    print "Waiting for response from",addr
                                    response = client_sock.recv(1024).decode()
                                    print "Received response:",response
                                    if response == 'Ack' :
                                        print "Received Acknowledgement from ",addr
                                        if self.msgQ.empty() :
                                            client_sock.send('Message Queue is Empty')
                                        else :
                                            client_sock.send('Ack')
                                            response2 = None
                                            while response2 is None :
                                                print "Waiting for response from",addr
                                                response2 = client_sock.recv(1024).decode()
                                                print "Received response:",response2
                                                if response2 == 'Ack' :
                                                    print "Sending Message Queue size", self.msgQ.qsize()
                                                    client_sock.send(str(self.msgQ.qsize()))
                                                    response3 = None
                                                    while response3 is None :
                                                        response3 = client_sock.recv(1024).decode()
                                                        print "Received response:",response3
                                                        if response3 == 'Ack' :
                                                            while not self.msgQ.empty() :
                                                                client_sock.send(str(self.msgQ.get()))
                                                                response4 = None
                                                                while response4 is None :
                                                                    response4 = client_sock.recv(1024).decode()
                                                                    print "Received response:",response3
                                
                            #    __handle_view(self)
                            # add view message to queue
                            #self.mailbox.connect(self.host_ip,self.server_port)
                            #self.mailbox.send("1")
                            #response = self.mailbox.recv(40)
                            #if response.decode() == "Ack" :
                            #    self.mailbox.send("Ack")
                                pass
                            elif input_data == '2' :
                            #    __handle_block(self)
                                print "Sending Block Acknowledgement to",addr
                                client_sock.send('Ack')
                                response = None
                                while response is None :
                                    print "Waiting for response from",addr
                                    response = client_sock.recv(1024).decode()
                                    print "Received response:",response
                                    buffer_size = int(response)
                                print "Sending Block Buffer Size Acknowledgement to",addr
                                client_sock.send('Ack')
                                entry = None
                                while entry is None :
                                    entry=client_sock.recv(buffer_size).decode()
                                    print "Received Block:", entry.decode()
                                time = datetime.utcnow()
                                self.msgQ.put((time,2,entry))
                                pass
                            elif input_data == '3' :
                            #    __handle_unblock(self)
                                print "Sending Unblock Acknowledgement to",addr
                                client_sock.send('Ack')
                                response = None
                                while response is None :
                                    print "Waiting for response from",addr
                                    response = client_sock.recv(1024).decode()
                                    print "Received response:",response
                                    buffer_size = int(response)
                                print "Sending Unblock Buffer Size Acknowledgement to",addr
                                client_sock.send('Ack')
                                entry = None
                                while entry is None :
                                    entry=client_sock.recv(buffer_size).decode()
                                    print "Received Unblock:", entry.decode()
                                time = datetime.utcnow()
                                self.msgQ.put((time,3,entry))
                                pass
                            elif input_data == '4' :
                                print "Sending Receive Tweet Acknowledgement to ",addr
                                client_sock.send('Ack')
                                response = None
                                while response is None :
                                    print "Waiting for response from ",addr
                                    response = client_sock.recv(1024).decode()
                                    print "Received response:",response
                                    if response == 'Ack' :
                                        print "Received Acknowledgement from ",addr
                                        if not self.msgQ.empty() :
                                            client_sock.send("Not Empty")
                                            print msgQ.get()
                                        else :
                                            client_sock.send("Empty")
                                pass
                    else :
                        raise error(addr,"is no longer sending data")
                except : 
                    client_sock.close()
                    return False

        __listen(self,client_sock,addr)

        #Figure out request type
        #msg_type =     client_sock.recv(38).decode()
        
        #if not msg_type in VALID_TYPES:
        #    print("Invalid message type: " + msg_type + "\n")
        #    close(client_sock)
        #else :
        #    command[msg_type]
        #Get data buffer size
        #BUFFER_SIZE = client_sock.recv(1024).decode()
        #print("Received buffer size of {}")
        

        #Receive request
        #self.client_sock.recv(BUFFER_SIZE)
        #client_sock.close()
    def run(self):
        self.mailbox.listen(20)
        print("Mailbox listening on {}:{}".format(self.host_ip,self.mail_port))
        while True :
            client_sock, addr = self.mailbox.accept()
            client_handler = threading.Thread(
                #target= self.__handle_req(),
                #args=(client_sock,)
                target= self.__handle_req(client_sock, addr)
            )
            self.threads.append(client_handler)
            
            client_handler.start()


if __name__ == '__main__':
    mailbox = Mailbox()
    mailbox.run()
