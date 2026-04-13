import socket
import json
import cliente
from cliente.broadcast_receiver import BroadcastReceiver

class Interface:
	def __init__(self):
		self.connection = socket.socket()
		self.broadcast_conn = socket.socket()  # socket dedicada ao broadcast

		self.ip = input("Insira o endereço IP do servidor: ")

		self.connection.connect((self.ip, cliente.PORT))
		self.broadcast_conn.connect((self.ip, cliente.BROADCAST_PORT))

#--------- Funções de envio e receção de dados ---------

	def receive_str(self,connect, n_bytes: int) -> str:
		data = connect.recv(n_bytes)
		return data.decode()

	def send_str(self,connect, value: str) -> None:
		connect.send(value.encode())

	def send_int(self,connect:socket.socket, value: int, n_bytes: int) -> None:
		connect.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

	def receive_int(self,connect: socket.socket, n_bytes: int) -> int:
		data = connect.recv(n_bytes)
		return int.from_bytes(data, byteorder='big', signed=True)

	def send_object(self,connection, obj):
		"""1º: envia tamanho, 2º: envia dados."""
		data = json.dumps(obj).encode('utf-8')
		size = len(data)
		self.send_int(connection, size, cliente.INT_SIZE)
		connection.send(data)

	def receive_object(self,connection):
		"""1º: lê tamanho, 2º: lê dados."""
		size = self.receive_int(connection, cliente.INT_SIZE)
		data = connection.recv(size)
		return json.loads(data.decode('utf-8'))

#--------------------------------------------------------

	def execute(self):
		player_name = input("Insira o nome do jogador (MAX 10 chars): ")
		player_name_padded = player_name[:10].ljust(10)
		self.send_str(self.connection, player_name_padded)

		print("Preciso que escolha uma das classes apresentadas:")
		classes = self.receive_object(self.connection)

		counter = 1
		while True:
			for classe in classes:
				print(f"{counter} - {classe['nome']} - {classe['descricao']}")
				counter += 1

			option = input()

			if option.isdigit() and 1 <= int(option) <= len(classes):
				selected_class = classes[int(option) - 1]
				self.send_object(self.connection, selected_class)
				print(f"Você escolheu a classe: {selected_class['nome']}")
				break
			else:
				print("Opção inválida. Por favor, escolha um número válido.")
				counter = 1

		receiver = BroadcastReceiver(self.broadcast_conn)
		receiver.start()

		while True:
			print("Indique a posição por onde quer ir (W,A,S ou D) e pressione enter ('.' para fim)")
			res:str = input()
			if res == "w":
				self.send_str(self.connection, cliente.MOVE_UP)
			if res == "s":
				self.send_str(self.connection, cliente.MOVE_DOWN)
			if res == "a":
				self.send_str(self.connection, cliente.MOVE_LEFT)
			if res == "d":
				self.send_str(self.connection, cliente.MOVE_RIGHT)

			if res == ".":
				self.send_str(self.connection, cliente.BYE_OP)
				print("Encerrando conexão.")
				self.connection.close()
				self.broadcast_conn.close()
				break

			if res == "sys_out":
				self.send_str(self.connection, cliente.END_OP)
				print("Fechando servidor e encerrando conexão.")
				self.connection.close()
				self.broadcast_conn.close()
				break
