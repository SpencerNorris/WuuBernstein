'''
Authors: Spencer Norris, Sabbir Rashid
File: mailbox.py
Description: mailbox for handling message reception from remote processes.
'''

import socket
import sys

class Mailbox:
	def __init__():
		self.client_ip = '127.0.0.1'
		self.client_port = 9999
		self.mail_port = 9000
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.bind((bind_ip, bind_port))
		server.listen(20) 
		print("Mailbox listening on {}:{}".format(bind_ip,bind_port))

	def __handle_req(client_sock):
		'''
		Implementation of handshakes for receiving 'show' requests from client,
		receiving 'tweet' requests from other nodes,
		and sending 'show' and 'tweet' requests to server.
		'''

		def __handle_show(buff_size):
			pass

		def __handle_tweet(buff_size):
			pass

		def __handle_block(buff_size):
			pass
		def __handle_unblock(buff_size):
			pass

		#Figure out request type


		#Get data buffer size
		BUFFER_SIZE = client_sock.recv(1024).decode()
		print("Received buffer size of {}")
		client_sock.send('ACK')

		#Receive request
		client_sock.recv(BUFFER_SIZE)
		client_sock.close()

	def run():
		while(True):
			client_sock, addr = server.accept()
			client_handler = threading.Thread(
        		target= __handle_req,
        		args=(client_sock,)
    		)
    		client_handler.start()


if __name__ == '__main__':
	mailbox = Mailbox()
	mailbox.run()
