import threading
import json
import cliente  # Para INT_SIZE

class BroadcastReceiver(threading.Thread):
    def __init__(self, connection):  # Só precisa da socket connection
        super().__init__(daemon=True)
        self.connection = connection

    def receive_int(self, n_bytes: int) -> int:
        data = self.connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def receive_object(self):
        """1º: lê tamanho, 2º: lê dados (igual ao da Interface)."""
        size = self.receive_int(cliente.INT_SIZE)
        data = self.connection.recv(size)
        return json.loads(data.decode('utf-8'))

    def run(self):
        print("Receiver de broadcasts ativa (a cada ~10s)...")
        while True:
            try:

                hist = self.receive_object()
                print("\n--- Broadcast do servidor ---")
                print(f"Histórico: {hist}")
                print("-----------------------------")
            except (Exception) as e:
                print(f"Receiver desconectado: {e}")
                break
