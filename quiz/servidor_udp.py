from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time
import random

class ServidorUDP:
	clients = list
	server_socket = None
	buffer_size = 2048 # Tamanho do buffer (bytes)

	def __init__(self, address, port):
		self.server_socket = socket(AF_INET, SOCK_DGRAM)
		self.server_socket.bind((address, port)) # Vinculando socket a um IP:Porta

		self.clients = []
		
		print('Servidor Iniciado\nAguardando Clientes...\n')

		while True:
			client_sock = self.server_socket.recvfrom(self.buffer_size)
			comm = client_sock[0].decode()
			client = client_sock[1]

			print(comm)

			# Adicionando novo cliente, caso haja espaco
			if client not in self.clients:
				if len(self.clients) < 6:
					self.new_client(client_sock)
				else:
					print('Jogo lotado, tente mais tarde')
					break
			else:
				if comm == 'pronto':
					print(f'Cliente {client} iniciou o jogo!')
					if len(self.clients) > 1:
						self.play_game()

	
	@staticmethod
	def print_clients(self):
		i = 0
		print('Clientes atualmente na sessao:')
		if len(self.clients) > 0:
			for client in self.clients:
				print(f'Cliente {i}:\n{client} ok\n----\n')
				i += 1
		else:
			print('Nao há clientes na sessao')

	# Funcao que adiciona um novo cliente a nossa lista e confirma conexao
	@staticmethod
	def new_client(self, client):
		self.clients.append(client[1])
		print(f'Novo cliente conectado: {client[1]}\nMsg: {client[0].decode()}')
		msg = 'Ola cliente voce esta conectado'
		self.server_socket.sendto(msg.encode(), client[1])
	
	@staticmethod
	def play_game(self):
		self.broadcast("Bem vindos! Vamos comecar o jogo em 10 segundos!")
		self.print_clients()


	@staticmethod
	# Envia mensagem a todos os clientes na lista (conectados)
	def broadcast(self, data):
		for client in self.clients:
			self.server_socket.sendto(data.encode(), client)
				

serv = ServidorUDP('localhost', 9500)