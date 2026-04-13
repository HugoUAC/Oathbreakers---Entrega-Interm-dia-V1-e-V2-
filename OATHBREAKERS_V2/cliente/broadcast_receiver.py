import threading
import json
import cliente

class BroadcastReceiver(threading.Thread):
    def __init__(self, connection):
        super().__init__(daemon=True)
        self.connection = connection

    def receive_int(self, n_bytes: int) -> int:
        data = self.connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def receive_object(self):
        """1º: lê tamanho, 2º: lê dados."""
        size = self.receive_int(cliente.INT_SIZE)
        data = b""
        while len(data) < size:
            packet = self.connection.recv(size - len(data))
            if not packet:
                raise ConnectionError("Ligação de broadcast fechada")
            data += packet
        return json.loads(data.decode('utf-8'))

    def run(self):
        print("Receiver de broadcasts ativa...")
        while True:
            try:
                players = self.receive_object()
                print("\n--- Broadcast do servidor ---")
                for p in players:
                    print(f"  {p['nome']} | Classe: {p['classe']} | Posição: {p['posicao']} | Status: {p['status']} | HP: {p['vida']} | MP: {p['mana']}")
                print("-----------------------------")
            except Exception as e:
                print(f"Receiver desconectado: {e}")
                break
