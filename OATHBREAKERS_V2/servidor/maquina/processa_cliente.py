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
        self.dados = dados
        self.mov = Movimento(connection, address)
        self.sum = Somar()
        self.sub = Subtrair()

    #----------interaction with sockets ---------------
    def receive_int(self,connection, n_bytes: int) -> int:
        data = connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_int(self,connection, value: int, n_bytes: int) -> None:
        connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_str(self,connection, n_bytes: int) -> str:
        data = connection.recv(n_bytes)
        return data.decode()

    def send_str(self,connection, value: str) -> None:
        connection.sendall(value.encode())

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
    #--------

    def run(self):
        print(self.address, "Thread iniciada")
        name = self.receive_str(self.connection, servidor.COMMAND_SIZE)

        self.send_object(self.connection, self.dados.classes)
        classe = self.receive_object(self.connection)

        player = {
            "jogador": self.address,
            "conexao": self.connection,
            "nome": name.strip(),
            "posicao": [0,0],
            "classe": classe["nome"],
            "nivel": 0,
            "ouro": 0,
            "experiencia": 0,
            "vida": classe["vida"],
            "mana": classe["mana"],
            "inventario": [],
            "status": "vasculhando"
        }
        self.dados.registar_player(player)

        last_request = False
        while not last_request:
            request_type = self.receive_str(self.connection, servidor.COMMAND_SIZE)

            if request_type == servidor.MOVE_UP:
                for p in self.dados.get_players_info():
                    if p["jogador"] == self.address:
                        self.mov.move_up(p)
                        print(p)
            elif request_type == servidor.MOVE_DOWN:
                for p in self.dados.get_players_info():
                    if p["jogador"] == self.address:
                        self.mov.move_down(p)
            elif request_type == servidor.MOVE_LEFT:
                for p in self.dados.get_players_info():
                    if p["jogador"] == self.address:
                        self.mov.move_left(p)
            elif request_type == servidor.MOVE_RIGHT:
                for p in self.dados.get_players_info():
                    if p["jogador"] == self.address:
                        self.mov.move_right(p)
            elif request_type == servidor.BYE_OP:
                last_request = True
                self.dados.remover_player(self.address)
                print(self.address, "Thread terminada")
                self.connection.close()
            elif request_type == servidor.END_OP:
                pass
