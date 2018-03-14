# server.py
 
import sys
import socket
import select
import re
from utils import *

class Server:
    
    socket_list = []
    channels = []
    client_channel_map = {}
    host = "localhost"
    
    def __init__(self, port):
        self.host = socket.gethostbyname(self.host)
        self.port = int(port)
        
        # initialize the server socket with given host and port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        
        # make it listen to 5 connections
        self.server_socket.listen(5)
        
        # add server socket to the list of readable connections
        self.socket_list.append(self.server_socket)
    
    def start_chat(self):
        while True:
            # get the list of sockets ready to be read through select.select
            ready_to_read, ready_to_write, in_error = select.select(self.socket_list, [], [])
            
            for socket in ready_to_read:
                if socket == self.server_socket:
                    self.connection_request()
                    
                # message is from an existing client connection
                else:
                    try:
                        message = socket.recv(MESSAGE_LENGTH)
                        client_address = str(socket.getpeername())
                        client_name = message.split(" ", 1)[0].replace("[", "").replace("]", "")

                        if message:
                            # message is a control message
                            if re.match(r'/', message.split(" ", 1)[1].rstrip()):
                                self.control_message(message, client_name, client_address, socket)
                            
                            # if not an ordinary message
                            else:
                                if self.client_channel_map.get(client_address):
                                    if "Disconnect!" in message.rstrip():
                                        self.broadcast(socket, SERVER_CLIENT_LEFT_CHANNEL.format(client_name) + "\n    ")
                                        self.socket_list.remove(socket)
                                        self.client_channel_map.pop(socket)
                                    else:
                                        self.broadcast(socket, message + "    ")
                                else:
                                    self.send_to_client(socket, SERVER_CLIENT_NOT_IN_CHANNEL + "\n    ")
                    except:
                        continue
    
    
    # if a new connection request is received
    # socket == self.server_socket works because client socket is binded or has 
    # the same host and ip such as this client
    def connection_request(self):
        (new_client_socket, (address)) = self.server_socket.accept()
        self.socket_list.append(new_client_socket)
        self.send_to_client(new_client_socket, "Welcome to the chat app! Your address is " + str(address) + ".\n    ")
    
    # handles control messages 
    def control_message(self, message, name, address, socket):
        # send channel list to client
        if re.match(r'/list$', message.split(" ", 1)[1].rstrip()):
            for channel in self.channels:
                self.send_to_client(socket, channel + "\n    ")
        # client wants to create a new channel
        # elif "/create" in message:
        elif re.match(r'^(/create)', message.split(" ", 1)[1].rstrip()):
            if re.match(r'/create\s\S+', message.split(" ", 1)[1].rstrip()):     
                channel = message.split("/create ")[1].rstrip()
                if channel in self.channels:
                    self.send_to_client(socket, SERVER_CHANNEL_EXISTS.format(channel) + ".\n    ")
                else:
                    if self.client_channel_map.get(address):
                        self.broadcast(socket, SERVER_CLIENT_LEFT_CHANNEL.format(name) + "\n    ")
            
                    self.channels.append(channel)
                    self.client_channel_map[address] = channel
                    self.send_to_client(socket, "You created a new channel named " + channel + ".\n    ")
            else:
                self.send_to_client(socket, SERVER_CREATE_REQUIRES_ARGUMENT + ".\n    ")
        # join an existing channel 
        # elif "/join" in message:
        elif re.match(r'^(/join)', message.split(" ", 1)[1].rstrip()):
            if re.match(r'/join\s\S+', message.split(" ", 1)[1].rstrip()):    
                channel = message.split("/join ")[1].rstrip()
                if channel in self.channels:
                    if self.client_channel_map.get(address):
                        self.broadcast(socket, SERVER_CLIENT_LEFT_CHANNEL.format(name) + ".\n    ")
                        
                    self.client_channel_map[address] = channel
                    self.send_to_client(socket, "You joined a channel named " + channel + ".\n    ")
                    self.broadcast(socket, SERVER_CLIENT_JOINED_CHANNEL.format(name) + ".\n    ")
                else:
                    self.send_to_client(socket, SERVER_NO_CHANNEL_EXISTS.format(channel) + ".\n    ")
            else:
                self.send_to_client(socket, SERVER_JOIN_REQUIRES_ARGUMENT + ".\n    ")
        else:
            self.send_to_client(socket, SERVER_INVALID_CONTROL_MESSAGE.format(message.split(" ", 1)[1].rstrip()) + "\n    ")
            
    # send message to all clients                        
    def broadcast(self, client_socket, message):
        for socket in self.socket_list:
            # send messages only to peers
            if socket != self.server_socket and socket != client_socket:
                if self.client_channel_map[str(client_socket.getpeername())] == self.client_channel_map[str(socket.getpeername())]:
                    try:
                        socket.send(message)
                    except:
                        socket.close()
                        if socket in self.socket_list:
                            self.socket_list.remove(socket)
                            self.client_channel_map.pop(socket)
        
    # send to a specific client
    def send_to_client(self, client_socket, message):
        try:
            client_socket.send(message)
        except:
            client_socket.close()
            if client_socket in self.socket_list:
                self.socket_list.remove(client_socket)
                self.client_channel_map.pop(client_socket)

if len(sys.argv) < 3:
    server = Server(sys.argv[1])
    server.start_chat()