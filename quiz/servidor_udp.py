from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time
import random

class ServidorUDP:
	clients = list
	server_socket = None
	buffer_size = 2048 # Tamanho do buffer (bytes)
	questions = list
	bool_qst = list

	def __init__(self, address, port):
		self.server_socket = socket(AF_INET, SOCK_DGRAM)
		self.server_socket.bind((address, port)) # Vinculando socket a um IP:Porta

		self.clients = []
		self.questions = [None for i in range(21)] # slot zero fica vazio
		self.bool_qst = [False for i in range(21)] # marcador de perguntas usadas no jogo

		# Carregando perguntas e respostas
		self.load_quiz(self)
		
		print('Servidor Iniciado\nAguardando Clientes...\n')

		while True:
			client_sock = self.server_socket.recvfrom(self.buffer_size)
			comm = client_sock[0].decode()
			client = client_sock[1]

			print(comm)

			# Adicionando novo cliente, caso haja espaco
			if client not in self.clients:
				if len(self.clients) < 6:
					self.new_client(self, client)
				else:
					print('Jogo lotado, tente mais tarde')
					break
			else:
				if comm == 'iniciar':
					if len(self.clients) > 1:
						print(f'Jogador {client} iniciou o jogo!')
						self.play_game(self)
					else:
						print("Nao ha jogadores suficientes")
				
				elif comm == 'quit':
					print(f'Jogador {client} saiu.')

	
	@staticmethod
	def print_clients(self):
		i = 0
		msg = '\nClientes atualmente na sessao:\n'
		if len(self.clients) > 0:
			for client in self.clients:
				msg += f'Cliente {i}:\n{client} ok\n----\n'
				i += 1
		else:
			msg += '\nNao há clientes na sessao\n'
		msg += "\n\n"
		return msg

	# Funcao que adiciona um novo cliente a nossa lista e confirma conexao
	@staticmethod
	def new_client(self, client):
		self.clients.append(client)
		print(f'Novo cliente conectado: {client}')
		msg = 'Ola cliente voce esta conectado'
		self.server_socket.sendto(msg.encode(), client)
	
	@staticmethod
	def play_game(self):
		self.broadcast(self, "Bem vindos! Vamos comecar o jogo em 10 segundos!\n")
		self.broadcast(self, self.print_clients(self))
		time.sleep(10)
		print("Jogo Iniciado")
		self.new_round(self)

	@staticmethod
	def new_round(self):
		self.broadcast(self, "Rodada iniciada!\n")
		run = True
		while run: # pensar se em algum momento ficarei sem perguntas (vai bugar)
			id = random.randint(1, 3)
			if self.bool_qst[id]:	
				pergunta = self.questions[id]
				run = False

		self.broadcast(self, f'Pergunta: {pergunta[0]}')
	
	@staticmethod
	def load_quiz(self):
		qst_file = open("quiz.txt")
		i = 1
		for line in qst_file:
			self.questions[i] = line.split(', ')
			i += 1
		print(f'\nQuiz carregado: \n\n')
		for key in range(1,21):
			print(f'Pergunta[{key}]: {self.questions[key]}')

	@staticmethod
	# Envia mensagem a todos os clientes na lista (conectados)
	def broadcast(self, data):
		for client in self.clients:
			self.server_socket.sendto(data.encode(), client)
				

serv = ServidorUDP('localhost', 9500)