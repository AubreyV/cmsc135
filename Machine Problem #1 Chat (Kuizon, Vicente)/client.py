# client.py

import sys
import socket
import select
import re
from utils import *
 
class Client:
    
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = int(port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channel = None
    
    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
        except:
            print CLIENT_CANNOT_CONNECT.format(self.host, self.port)
            sys.exit()
    
    def start_chat(self):
        sys.stdout.write(CLIENT_MESSAGE_PREFIX); sys.stdout.flush()
        sys.stdout.write(CLIENT_WIPE_ME)
        
        while True:
            socket_list = [sys.stdin, self.client_socket]
            
            ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])
            
            for socket in ready_to_read:
                # a message from the peers through the server has been sent
                if socket == self.client_socket:
                    message = socket.recv(MESSAGE_LENGTH)
                    if not message:
                        print CLIENT_SERVER_DISCONNECTED.format(self.host, self.port)
                        sys.exit()
                    else:
                        sys.stdout.write(message)
                        sys.stdout.write(CLIENT_MESSAGE_PREFIX); sys.stdout.flush()
                        sys.stdout.write(CLIENT_WIPE_ME)
                
                # send a message to peers through the server
                else:
                    self.messageToSend = sys.stdin.readline().rstrip()
                    self.send_to_client_split()
                    # self.client_socket.send("[" + self.name + "] " + message)
                    sys.stdout.write(CLIENT_MESSAGE_PREFIX); sys.stdout.flush()
                    sys.stdout.write(CLIENT_WIPE_ME)
    
    def send_to_client_split(self):
        length = len(self.messageToSend)
        count = 0
        
        if length < MESSAGE_LENGTH:
            self.client_socket.send("[" + self.name + "] " + self.messageToSend + "\n")
        else:
            while count < length:
                if (count + MESSAGE_LENGTH) > length:
                    self.client_socket.send("[" + self.name + "] " + self.messageToSend[count:] + "\n")
                else:
                    self.client_socket.send("[" + self.name + "] " + self.messageToSend[count: -(count + MESSAGE_LENGTH)] + "\n")
                count = count + MESSAGE_LENGTH
        
if len(sys.argv) < 5:
    try:
        client = Client(sys.argv[1], sys.argv[2], sys.argv[3])
        client.connect_to_server()
        client.start_chat()
    except:
        client.client_socket.send(client.name + " Disconnect!")
        client.client_socket.close()