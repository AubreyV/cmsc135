import socket
import sys

class Server:
	server = socket.socket()
	host = "127.0.0.1"

	def __init__(self, port):
		#super(Server, self).__init__()
		self.port = int(port)
		self.server.bind((self.host, self.port))
		self.server.listen(5)

	def receive(self):
		while True:
			(new_socket, address) = self.server.accept()
			message = new_socket.recv(1024)
			print "[" + message.split(":")[0] + "]: " + message.split(":")[1]

if __name__ == "__main__":
	if len(sys.argv) < 3:
		s = Server(sys.argv[1])
		s.receive()