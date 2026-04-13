import servidor
import socket
import json
import threading
from servidor.operacoes.movimento import Movimento
from servidor.operacoes.somar import Somar
from servidor.operacoes.subtrair import Subtrair

class ProcessaCliente(threading.Thread):
    def __init__(self, connection, address, dados):
        super().__init__()
        self.connection = connection
        self.address = address
        self.s = socket.socket()
        self.dados = dados
        self.mov = Movimento(connection, address, self.s)
        self.sum = Somar()
        self.sub = Subtrair()

    #----------interaction with sockets ---------------
    # all functions interacting with sockets
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
        connection.sendall(value.encode())

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
    #--------

    def run(self):
        print(self.address, "Thread iniciada")
        name = self.receive_str(self.connection, servidor.COMMAND_SIZE)  # Recebe o comando de início do cliente

        self.send_object(self.connection, self.dados.classes)  # Envia as classes disponíveis para o cliente
        classe = self.receive_object(self.connection)  # Recebe a classe escolhida pelo cliente
        player = {
            "jogador": self.address,
            "conexao": self.connection,
			"nome": name,
			"posicao": [0,0], #posição inicial
			"classe": classe["nome"],
			"nivel": 0,
			"ouro": 0,
			"experiencia": 0,
			"vida": classe["vida"],
			"mana": classe["mana"],
			"inventario": [], #LIMITE DE POR EXEMPLO 10
			"status": "vasculhando" #ou "em combate"		
        }
        self.dados.registar_player(player)

        last_request = False
        while not last_request:
            request_type = self.receive_str(self.connection, servidor.COMMAND_SIZE)

            if request_type == servidor.MOVE_UP:
                for player in self.dados.get_players_info():
                    if player["jogador"] == self.address:
                        self.mov.move_up(player)
                        print(player)
            elif request_type == servidor.MOVE_DOWN:
                for player in self.dados.get_players_info():
                    if player["jogador"] == self.address:
                        self.mov.move_down(player)
            elif request_type == servidor.MOVE_LEFT:
                for player in self.dados.get_players_info():
                    if player["jogador"] == self.address:
                        self.mov.move_left(player)
            elif request_type == servidor.MOVE_RIGHT:
                for player in self.dados.get_players_info():
                    if player["jogador"] == self.address:
                        self.mov.move_right(player)
            
            elif request_type == servidor.BYE_OP:
                last_request = True
                print(self.address, "Thread terminada")
                self.connection.close()
            elif request_type == servidor.END_OP:
                pass