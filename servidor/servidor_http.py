from socket import socket, AF_INET, SOCK_STREAM

server_socket = socket(AF_INET, SOCK_STREAM)

server_socket.bind(('localhost', 9000))

server_socket.listen()

socket_client, client_address = server_socket.accept()

data = socket_client.recv(2048)
print(f'{data.decode()}')

msg = ('HTTP/1.1 200 OK\r\n'
	   'Date: 23/11/2021\r\n'
	   'Server: Jaca/0.0.1\r\n'
	   'Content-Type: text\r\n'
	   '\r\n')

msg += ('<html><head><title>Eu sou um exemplo</title></head>'
		'<body><h1>Eu sou um titulo menor</h1>'
		'<h3>Eu sou um titulo menor</h3>'
		'</body>'
		'</html>')

socket_client.send(msg.encode())

# pra testar, 


