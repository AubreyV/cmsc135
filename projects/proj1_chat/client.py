import socket
import sys

class Client:

	def __init__(self, name, host, port):
		#super(Client, self).__init__()
		self.name = name
		self.host = host
		self.port = int(port)
		self.socket = socket.socket()
				
	def send(self, message):
		self.socket.connect((self.host, self.port))
		self.socket.sendall(self.name + ":" + message)

if len(sys.argv) < 5:
	c = Client(sys.argv[1], sys.argv[2], sys.argv[3])
	message = raw_input()
	c.send(message)
