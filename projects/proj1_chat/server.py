from echoserver import EchoServer
from broadcastserver import BroadcastServer
from dummy import Dummy
import socket
import sys
import threading

class Server:
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	receive = False

	def __init__(self, host, port, b):
		self.host = socket.gethostbyname(host)
		self.port = int(port)
		self.server.bind((self.host, self.port))
		self.server.listen(5)
		self.b = b

	def accept_clients(self):
		while True:
			(new_socket, (ip, port)) = self.server.accept()
			print ip + " connected at port " + str(port)
			self.b.add_to_list(new_socket)
			self.b.welcome_message("Welcome to the chat room!", new_socket)
			
			# b.start()
			# message = new_socket.recv(1024)
			# print "[" + message.split(":")[0] + "]: " + message.split(":")[1]

	def receive_messages(self):
		if self.receive:
			pass
		while self.receive:
			message = self.server.recv(2048)
			print message

if len(sys.argv) < 4:
	b = BroadcastServer()
	s = Server(sys.argv[1], sys.argv[2], b)
	t1 = threading.Thread(target=s.accept_clients)
	t2 = threading.Thread(target=s.receive_messages)
	t1.start()
	t2.start()