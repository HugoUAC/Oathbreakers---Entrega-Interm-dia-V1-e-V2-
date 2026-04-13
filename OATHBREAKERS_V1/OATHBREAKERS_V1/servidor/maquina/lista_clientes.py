# lista_clientes.py
import threading
from typing import Dict, Tuple
import socket

class ListaClientes:
    def __init__(self):
        self.clientes: Dict[Tuple[str, int], socket.socket] = {}
        self._lock = threading.Lock()
        self._nr_clientes = 0



    def adicionar(self, client: Tuple[str, int], connection: socket.socket) -> None:
        with self._lock:
            self.clientes[client] = connection
            self._nr_clientes += 1
            # Test
            print("Client ", client," added to dictionary!")
            print("Nr. de clientes:",self._nr_clientes)

    def remover(self, addr: Tuple[str, int]) -> None:
        with self._lock:
            if addr in self.clientes:
                del self.clientes[addr]
                self._nr_clientes -= 1

    def obter_lista(self) -> Dict[Tuple[str, int], socket.socket]:
        # snapshot (shallow copy) só para leitura
        with self._lock:
            return self.clientes.copy()

    def obter_nr_clientes(self) -> int:
        return self._nr_clientes
