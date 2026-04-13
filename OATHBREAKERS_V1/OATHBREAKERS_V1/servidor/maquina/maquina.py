from servidor.dados.dados import Dados
from servidor.maquina.processa_cliente import ProcessaCliente
from servidor.operacoes.somar import Somar
from servidor.operacoes.dividir import Dividir
from servidor.maquina.lista_clientes import ListaClientes as LC
from servidor.maquina.broadcast_emissor import ThreadBroadcast
import servidor
import json
import socket

class Maquina:
	def __init__(self):
		self.sum = Somar()
		self.div = Dividir()
		self.dados = Dados()
		self.s = socket.socket()
		self.s.bind(('', servidor.PORT))
		self.broadcast = ThreadBroadcast(self.dados, intervalo=3)
		self.broadcast.start()

	# ---------------------- interaction with sockets ------------------------------
	def receive_int(self,connection, n_bytes: int) -> int:
		"""
		:param n_bytes: The number of bytes to read from the current connection
		:return: The next integer read from the current connection
		"""
		data = connection.recv(n_bytes)
		return int.from_bytes(data, byteorder='big', signed=True)

	def send_int(self,connection, value: int, n_bytes: int) -> None:
		"""
		:param value: The integer value to be sent to the current connection
		:param n_bytes: The number of bytes to send
		"""
		connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

	def receive_str(self,connection, n_bytes: int) -> str:
		"""
		:param n_bytes: The number of bytes to read from the current connection
		:return: The next string read from the current connection
		"""
		data = connection.recv(n_bytes)
		return data.decode()

	def send_str(self,connection, value: str) -> None:
		"""
		:param value: The string value to send to the current connection
		"""
		connection.connection.send(value.encode())

	def send_object(self,connection, obj):
		"""1º: envia tamanho, 2º: envia dados."""
		data = json.dumps(obj).encode('utf-8')
		size = len(data)
		self.send_int(connection, size, servidor.INT_SIZE)         # Envio do tamanho
		connection.send(data)              		     # Envio do objeto

	def receive_object(self,connection):
		"""1º: lê tamanho, 2º: lê dados."""
		size = self.receive_int(connection, servidor.INT_SIZE)  	# Recebe o tamanho
		data = connection.recv(size)       			# Recebe o objeto
		return json.loads(data.decode('utf-8'))


	def execute(self):

		#NOTE: Aqui mostra o endereço IP do servidor para o cliente conseguir conectar-se
		print("Starting server on " + servidor.SERVER_ADDRESS + ":" + str(servidor.PORT))

		
		self.s.listen(5)
		print("Waiting for clients on port " + str(servidor.PORT))
		try:
			while True:
				print("On accept...")
				connection, address = self.s.accept()
				print("Client " + str(address) + " connected")
				ProcessaCliente(connection, address, self.dados).start()
		except KeyboardInterrupt:
			print("Stopping...")
		finally:
			self.s.close()
			print("Server stopped")
