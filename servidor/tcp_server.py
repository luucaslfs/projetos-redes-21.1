from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

class ServidorTCP:
	def __init__(self, address, port):
		server_socket = socket(AF_INET, SOCK_STREAM)
		server_socket.bind((address, port)) # Vinculando socket a um IP:Porta
		server_socket.listen()
		#buffer_size = 2048 # Tamanho do buffer (bytes)

		print('Aguardando novas requisições')

		while True:
			(client_socket, client_address) = server_socket.accept()
			print(f'Requisicao estabelecida com cliente {client_address}')

			Thread(target=self.receive_data, args=(client_socket, client_address)).start()


	@staticmethod
	def receive_data(client_socket, address):
		while True:
			data = client_socket.recv(2048)
			print(f'O cliente {address} enviou: {data.decode()}')
			client_socket.send('Recebi sua mensagem'.encode())

serv_tcp = ServidorTCP('localhost', 8080)
