James Michael K. Kuizon
Aubrey M. Vicente

server.py accepts 1 argument: the port.
client.py accepts 3 arguments: the name, host, and port.
Run the program as follows (omit the []):
	python server.py [port]
	python client.py [name] [host] [port]

Message types:
    1. control messages - any string that starts with '/'
        1.1. /create [channel_name]
        1.2. /join [channel_name]
        1.3. /list
    2. normal messages - any string that does not start with '/'