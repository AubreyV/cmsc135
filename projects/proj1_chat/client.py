import socket
import sys
import threading

class Client:

	def __init__(self, name, host, port):
		# super(Client, self).__init__()
		self.name = name
		self.host = host
		self.port = int(port)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.host, self.port))
				
	def receive_message(self):
		while True:
			message = self.socket.recv(2048)
			print message

	def send_message(self):
		while True:
			message = raw_input("[Me]: ")
			self.socket.sendall("[" + self.name + "]" + ": " + message)

if len(sys.argv) < 5:
	c = Client(sys.argv[1], sys.argv[2], sys.argv[3])
	t1 = threading.Thread(target=c.receive_message)
	t2 = threading.Thread(target=c.send_message)
	t1.start()
	t2.start()

