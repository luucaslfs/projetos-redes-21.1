from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

class ClientTCP:
	def __init__(self, address, port):
		sock = socket(AF_INET, SOCK_STREAM)

		print('Tentando iniciar conexao com o servidor')
		sock.connect((address, port))
		print('Conexao estabelecida')

		Thread(target=self.rec_data, args=(sock,)).start()

		while True:
			msg = input()
			sock.send(msg.encode())

	@staticmethod
	def rec_data(sock):
		while True:
			data = sock.recv(2048)
			print(f'Servidor enviou >>> {data.decode()}')

cliente_tcp = ClientTCP('localhost', 8080)
