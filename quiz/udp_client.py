from socket import socket, AF_INET, SOCK_DGRAM

sock = socket(AF_INET, SOCK_DGRAM)

while True:
	msg = input()
	sock.sendto(msg.encode(), ('localhost', 9500))

#sock.close()