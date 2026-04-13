# thread_broadcast.py
import servidor
import threading
import time
import json
from servidor.dados.dados import Dados

class ThreadBroadcast(threading.Thread):
    def __init__(self, dados: Dados, intervalo: int = 3):
        super().__init__(daemon=True)
        self.dados = dados
        self.intervalo = intervalo
        self.running = True
        # Lista de sockets dedicadas ao broadcast (separadas das sockets principais)
        self.broadcast_sockets = []
        self.broadcast_lock = threading.Lock()

    def adicionar_broadcast_socket(self, conn):
        with self.broadcast_lock:
            self.broadcast_sockets.append(conn)
            print(f"Broadcast socket adicionada. Total: {len(self.broadcast_sockets)}")

    def remover_broadcast_socket(self, conn):
        with self.broadcast_lock:
            if conn in self.broadcast_sockets:
                self.broadcast_sockets.remove(conn)

    def send_int(self, connection, value: int, n_bytes: int) -> None:
        connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def send_object(self, connection, obj):
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.send_int(connection, size, servidor.INT_SIZE)
        connection.send(data)

    def broadcast_object(self, obj) -> None:
        """Envia obj para todas as sockets de broadcast registadas."""
        with self.broadcast_lock:
            mortos = []
            for conn in self.broadcast_sockets:
                try:
                    self.send_object(conn, obj)
                except Exception:
                    print(f"Removendo broadcast socket morta")
                    conn.close()
                    mortos.append(conn)
            for conn in mortos:
                self.broadcast_sockets.remove(conn)

    def run(self):
        print("ThreadBroadcast ativa")
        while self.running:
            try:
                time.sleep(self.intervalo)
                players = self.dados.get_players_info()
                self.broadcast_object(players)
                print(f"Broadcast para {len(self.broadcast_sockets)} clientes")
            except Exception as e:
                print(f"Erro: {e}")
                continue
        print("ThreadBroadcast terminada")
