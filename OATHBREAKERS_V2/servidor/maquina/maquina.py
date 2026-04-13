from servidor.dados.dados import Dados
from servidor.maquina.processa_cliente import ProcessaCliente
from servidor.operacoes.somar import Somar
from servidor.operacoes.dividir import Dividir
from servidor.maquina.broadcast_emissor import ThreadBroadcast
import servidor
import json
import socket
import threading

class Maquina:
	def __init__(self):
		self.sum = Somar()
		self.div = Dividir()
		self.dados = Dados()
		self.s = socket.socket()
		self.s.bind(('', servidor.PORT))
		# Socket dedicada ao broadcast numa porta separada
		self.s_broadcast = socket.socket()
		self.s_broadcast.bind(('', servidor.BROADCAST_PORT))
		self.broadcast = ThreadBroadcast(self.dados, intervalo=3)
		self.broadcast.start()

	# ---------------------- interaction with sockets ------------------------------
	def receive_int(self,connection, n_bytes: int) -> int:
		data = connection.recv(n_bytes)
		return int.from_bytes(data, byteorder='big', signed=True)

	def send_int(self,connection, value: int, n_bytes: int) -> None:
		connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

	def receive_str(self,connection, n_bytes: int) -> str:
		data = connection.recv(n_bytes)
		return data.decode()

	def send_str(self,connection, value: str) -> None:
		connection.send(value.encode())

	def send_object(self,connection, obj):
		"""1º: envia tamanho, 2º: envia dados."""
		data = json.dumps(obj).encode('utf-8')
		size = len(data)
		self.send_int(connection, size, servidor.INT_SIZE)
		connection.send(data)

	def receive_object(self,connection):
		"""1º: lê tamanho, 2º: lê dados."""
		size = self.receive_int(connection, servidor.INT_SIZE)
		data = connection.recv(size)
		return json.loads(data.decode('utf-8'))

	def _aceitar_broadcast_connections(self):
		"""Thread que aceita ligações na porta de broadcast."""
		self.s_broadcast.listen(5)
		print(f"Aguardando ligações de broadcast na porta {servidor.BROADCAST_PORT}")
		while True:
			try:
				conn, addr = self.s_broadcast.accept()
				print(f"Broadcast socket ligada: {addr}")
				self.broadcast.adicionar_broadcast_socket(conn)
			except Exception as e:
				print(f"Erro ao aceitar broadcast: {e}")
				break

	def execute(self):
		print("Starting server on " + servidor.SERVER_ADDRESS + ":" + str(servidor.PORT))

		# Inicia thread que aceita ligações de broadcast
		t_broadcast_accept = threading.Thread(target=self._aceitar_broadcast_connections, daemon=True)
		t_broadcast_accept.start()

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
			self.s_broadcast.close()
			print("Server stopped")
