'''
Authors: Spencer Norris, Sabbir Rashid
File: mailbox.py
Description: mailbox for handling message reception from remote processes.
'''

import socket
import sys
import threading
#from multiprocessing import Queue
from Queue import PriorityQueue

class Mailbox:
    def __init__(self):
        self.host_ip = '127.0.0.1'
        self.mail_port = 9000
        self.client_port = 9999
        self.server_port = 5000
        self.mailbox = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mailbox.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.mailbox.bind((self.host_ip, self.mail_port))
        self.msgQ = PriorityQueue()
        self.threadQ = PriorityQueue()

        self.VALID_TYPES = ['0', '1', '2', '3', '4']

    def __handle_req(self,client_sock, addr):

        '''
        Implementation of handshakes for receiving 'show' requests from client,
        receiving 'tweet' requests from other nodes,
        and sending 'show' and 'tweet' requests to server.
        '''           
        def __handle_tweet(self):
            print "Sending Tweet Acknowledgement to Client ",addr
            client_sock.send('ACK')
            response = sock.recv(1024)
            buffer_size = atoi(response.decode())
            print "Sending Tweet Buffer Size Acknowledgement to Client ",addr
            client_sock.send('ACK')
            entry=sock.recv(buffer_size)
            print "Received tweet", entry.decode()
            # add tweet to message queue
            pass

        def __handle_view(self,buff_size):
            # add view message to queue
            self.mailbox.connect(self.host_ip,self.server_port)
            self.mailbox.send("1")
            response = self.mailbox.recv(40)
            if response.decode() == "Ack" :
                self.mailbox.send("Ack")
            pass

        def __handle_block(self,buff_size):
            client_sock.send('ACK')
            response = sock.recv(1024)
            buffer_size = atoi(response.decode())
            client_sock.send('ACK')
            entry=sock.recv(buffer_size)
            #print entry.decode()
            # add block to message queue
            pass

        def __handle_unblock(self,buff_size):
            client_sock.send('ACK')
            response = sock.recv(1024)
            buffer_size = atoi(response.decode())
            client_sock.send('ACK')
            entry=sock.recv(buffer_size)
            #print entry.decode()
            # add unblock to message queue
            pass

        def __handle_message(self,buff_size):
            client_sock.send('ACK')
            pass

        '''self.command = {
            '0': __handle_tweet,
            '1': __handle_view,
            '2': __handle_block,
            '3': __handle_unblock,
            '4' : __handle_message
            }'''

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
                            if input_data == '0' :
                                print "Sending Tweet Acknowledgement to Client ",addr
                                client_sock.send('Ack')
                                response = None
                                while response is None :
                                    print "Waiting for response from Client ",addr
                                    response = client_sock.recv(1024).decode()
                                    print "Received response:",response
                                    buffer_size = int(response)
                                print "Sending Tweet Buffer Size Acknowledgement to Client ",addr
                                client_sock.send('Ack')
                                entry = None
                                while entry is None :
                                    entry=client_sock.recv(buffer_size).decode()
                                    print "Received tweet:", entry.decode()
                                # add tweet to message queue
                            #pass
                            #self.command[input_data]
                            #print "Received input '",input_data,"' from Client ",addr
                            #response=input_data
                            #client_sock.send(response)
                    else :
                        raise error("Client ",addr," is no longer sending data")
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
            #threads.append(client_handler)
            
            client_handler.start()


if __name__ == '__main__':
    mailbox = Mailbox()
    mailbox.run()
