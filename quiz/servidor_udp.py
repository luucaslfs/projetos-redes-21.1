from socket import socket, AF_INET, SOCK_DGRAM

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('localhost', 9500))

while True:
	data, client_address= server_socket.recvfrom(2048)
	print(f'O cliente {client_address} mandou >>> {data.decode()}')
