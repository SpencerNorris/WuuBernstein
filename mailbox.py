'''
Authors: Spencer Norris, Sabbir Rashid
File: mailbox.py
Description: mailbox for handling message reception from remote processes.
'''

import socket
import sys
import threading

class Mailbox:
    def __init__(self):
        self.host_ip = '127.0.0.1'
        self.client_port = 9999
        self.mail_port = 9000
        self.server_port = 5000
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host_ip, self.mail_port))
        self.server.listen(20) 
        print("Mailbox listening on {}:{}".format(self.host_ip,self.mail_port))

    def __handle_req(self,client_sock):
        '''
        Implementation of handshakes for receiving 'show' requests from client,
        receiving 'tweet' requests from other nodes,
        and sending 'show' and 'tweet' requests to server.
        '''

        def __handle_tweet(self,buff_size):
            client_sock.send('ACK')
            response = sock.recv(1024)
            buffer_size = atoi(response.decode())
            client_sock.send('ACK')
            entry=sock.recv(buffer_size)
            #print entry.decode()
            # add tweet to message queue
            pass

        def __handle_view(self,buff_size):
            # add view message to queue
            self.server.connect(self.host_ip,self.server_port)
            self.server.send("1")
            response = self.server.recv(40)
            if response.decode() == "Ack" :
                self.server.send("Ack")
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
        
        command = {
                '0': __handle_tweet,
                '1': __handle_view,
                '2': __handle_block,
                '3': __handle_unblock,
                '4' : __handle_message
            }
        VALID_TYPES = ['0', '1', '2', '3', '4']
        #Figure out request type
        msg_type =     client_sock.recv(38).decode()
        
        if not msg_type in VALID_TYPES:
            print("Invalid message type: " + msg_type + "\n")
            close(client_sock)
        else :
            command[msg_type]
        #Get data buffer size
        #BUFFER_SIZE = client_sock.recv(1024).decode()
        #print("Received buffer size of {}")
        

        #Receive request
        #self.client_sock.recv(BUFFER_SIZE)
        client_sock.close()

    def run(self):
        threads = []
        while(True):
            client_sock, addr = self.server.accept()
            client_handler = threading.Thread(
                #target= __handle_req(),
                #args=(client_sock,)
                target= self.__handle_req(client_sock)
            )
            threads.append(client_handler)
            client_handler.start()


if __name__ == '__main__':
    mailbox = Mailbox()
    mailbox.run()
