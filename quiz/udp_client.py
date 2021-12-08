from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread

class ClientUDP:
	def __init__(self, server_address, port):
		sock = socket(AF_INET, SOCK_DGRAM)

		msg = 'Olá servidor'
		sock.sendto(msg.encode(), (server_address, port))
		Thread(target=self.rec_data, args=(sock,)).start()
		
		while True:
			msg = input()
			sock.sendto(msg.encode(), (server_address, port))

	@staticmethod
	def rec_data(sock):
		while True:
			data, server_address = sock.recvfrom(2048)
			print(f'Servidor {server_address} enviou >>> {data.decode()}')

cliente_tcp = ClientUDP('localhost', 9500)
