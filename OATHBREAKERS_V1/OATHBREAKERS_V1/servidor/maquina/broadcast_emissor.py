# thread_broadcast.py
import servidor
import threading
import time
import json
from typing import Dict
from servidor.dados.dados import Dados

class ThreadBroadcast(threading.Thread):
    def __init__(self, dados: Dados, intervalo: int = 3):
        super().__init__(daemon=True)
        self.dados = dados
        self.intervalo = intervalo
        self.running = True
    #-----
    def send_int(self,connection, value: int, n_bytes: int) -> None:
        connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def send_object(self, connection, obj):
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.send_int(connection,size, servidor.INT_SIZE)
        connection.send(data)


    def broadcast_object(self, obj: Dict) -> None:
        """
        Broadcast
        :param obj:
        :return:
        """
        with self.dados.lock:
            for player in self.dados.jogadores:
                try:
                    self.send_object(player["conexao"], obj)
                except Exception:
                    print(f"Removendo cliente morto {player['jogador']}")
                    player["conexao"].close()
                    #ABRIR LOCK PARA REMOVER CLIENTE E VOLTAR A FECHAR PARA EVITAR ERROS
                    #self.lista_clientes._lock.release()
                    #self.lista_clientes.remover(address)
                    #self.lista_clientes._lock.acquire()

    # broadcast_emissor.py - simplifica o run(), sem chamar get_players_info separado
    def run(self):
        print("ThreadBroadcast ativa")
        while self.running:
            try:
                time.sleep(self.intervalo)
                with self.dados.lock:
                    jogadores_copia = self.dados.jogadores[:]  # cópia com lock
                for player in jogadores_copia:
                    try:
                        self.send_object(player["conexao"], jogadores_copia)
                    except Exception:
                        print(f"Removendo cliente morto {player['jogador']}")
                        player["conexao"].close()
                print(f"Broadcast para {self.dados.nr_jogadores} jogadores")
            except Exception as e:
                print(f"Erro: {e}")
                continue
