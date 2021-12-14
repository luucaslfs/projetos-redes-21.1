from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
import time
import random

class ServidorUDP:
	clients = dict
	server_socket = None
	buffer_size = 2048 # Tamanho do buffer (bytes)
	questions = list
	bool_qst = list
	slots = list

	def __init__(self, address, port):
		self.server_socket = socket(AF_INET, SOCK_DGRAM)
		self.server_socket.bind((address, port)) # Vinculando socket a um IP:Porta

		self.clients = {}
		self.questions = [None for i in range(21)] # slot zero fica vazio
		self.bool_qst = [False for i in range(21)] # marcador de perguntas usadas no jogo
		self.slot = [None for i in range(5)]	   # slot de jogadores

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
				if comm == 'ola servidor':
					if len(self.clients) < 6:
						self.new_client(self, client)
					else:
						self.server_socket.sendto('Jogo lotado, tente mais tarde'.encode(), client)
						break
				else:
					self.server_socket.sendto(f'Comando {comm} nao reconhecido, para se conectar envie "ola servidor"'.encode(), client)
			else:
				if comm == 'iniciar':
					if len(self.clients) > 1:
						msg = f'Jogador {client} iniciou um novo jogo!'
						print(f"Cliente enviou: {msg}")
						self.broadcast(self, msg)
						self.play_game(self)
					else:
						msg = "Nao ha jogadores suficientes para iniciar o jogo"
						print(msg)
						self.broadcast(self, msg)
				
				elif comm == 'quit':
					self.clients.pop(client)
					print(f'Jogador {client} saiu.')				
	

	# Funcao que retorna lista de clientes conectados no momento
	@staticmethod
	def list_clients(self):
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
		self.clients[client] = {'Score': 0, 'Answer': None}
		print(f'Novo cliente conectado: {client}')
		msg = 'Conexao estabelecida com sucesso!'
		self.server_socket.sendto(msg.encode(), client)
	

	# Funcao que inicia e maneja um jogo inteiro, do inicio ao fim
	@staticmethod
	def play_game(self):
		self.broadcast(self, "Bem vindos! Vamos comecar o jogo em 10 segundos!\n")
		print("Jogo iniciando em 10 segundos!")
		print(self.list_clients(self))
		
		for key in self.clients:
			self.clients[key]['Score'] = 0
		self.bool_qst = [False for i in range(21)]

		time.sleep(10)
		
		print("Jogo Iniciado")
		for i in range(3):
			self.broadcast(self, f"\nRodada {i+1} iniciada!")
			self.new_round(self)
			self.broadcast(self, "*Proxima rodada iniciando em 10 segundos*")
			time.sleep(10)
		
		msg = "*** FIM DE JOGO ***\n"
		self.print_result(self)

	
	# Funcao que printa o ranking do momento, de acordo com os valores na nossa base de clientes, em ordem
	@staticmethod
	def print_result(self):
		msg = "\n** RANKING **\n"
		print(msg)
		self.broadcast(self, msg)

		ranking = {}
		for key in self.clients:
			ranking[key] = self.clients[key]['Score']

		i = 1
		for client in sorted(ranking, key = ranking.get, reverse=True):
			msg = f"{i}o lugar - {client}:  {ranking[client]} pontos"
			self.broadcast(self, msg)
			print(msg)
			i += 1
		

	# Funcao que inicia e maneja uma unica rodada
	@staticmethod
	def new_round(self):
		run = True
		while run:
			id = random.randint(1, 3)
			if not self.bool_qst[id]:	
				pergunta = self.questions[id]
				self.bool_qst[id] = True
				run = False
		
		self.broadcast(self, f'Pergunta: {pergunta[0]}')

		# Criando uma thread por cliente pra esperar a resposta deles
		i = 1
		for key in self.clients:
			print(f"Thread Resposta {i} iniciada")
			Thread(target=self.rec_answer, args=(self,)).start()
			i += 1

		time.sleep(6)
		self.broadcast(self, '\nRestam 4 segundos!\n')
		time.sleep(4)

		msg = "Rodada FINALIZADA\n"
		self.broadcast(self, msg)
		
		print("Respostas:\n")
		for key in self.clients:
			client = self.clients[key]
			print(f"Cliente {key} respondeu: {client['Answer']}")
			
			
			if client['Answer'] == None:
				msg = "Sem Resposta -1 ponto"
				self.server_socket.sendto(msg.encode(), key)
				print(msg)
				self.clients[key]['Score'] -= 1
			elif pergunta[1] == client['Answer']:
				msg = "Resposta Correta +25 pontos"
				self.server_socket.sendto(msg.encode(), key)
				print(msg)
				self.clients[key]['Score'] += 25
			else:
				msg = "Resposta Incorreta -5 pontos"
				self.server_socket.sendto(msg.encode(), key)
				print(msg)
				self.clients[key]['Score'] -= 5
			
			print("-------\n")
		

		
	# Funcao que roda numa thread para aguardar respostas dos clientes (jogadores)
	@staticmethod
	def rec_answer(self):
		sock = self.server_socket.recvfrom(self.buffer_size)
		client = sock[1]
		msg = sock[0]
		self.clients[client]['Answer'] = msg.decode()


	# Funcao que carrega o quiz a partir do arquivo 'quiz.txt'
	@staticmethod
	def load_quiz(self):
		qst_file = open("quiz.txt")
		i = 1
		for line in qst_file:
			self.questions[i] = line.split(', ')
			i += 1
		print(f'\nQuiz carregado: \n')
		for key in range(1,21):
			print(f'Pergunta[{key}]: {self.questions[key]}')
		print('\n')


	@staticmethod
	# Envia mensagem a todos os clientes na lista (conectados)
	def broadcast(self, data):
		for client in self.clients:
			self.server_socket.sendto(data.encode(), client)





serv = ServidorUDP('localhost', 9500)