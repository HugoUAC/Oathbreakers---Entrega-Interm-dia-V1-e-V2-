import threading
import json

class Dados:
    def __init__(self):
        self.jogadores = []
        self.nr_jogadores = 0
        self.classes = {}
        self.itens = {}
        self.inimigos = {}
        self.lock = threading.Lock()

        with open("servidor/dados/classes.json","r",encoding="utf-8") as f:
            self.classes = json.load(f)
        with open("servidor/dados/itens.json", "r", encoding="utf-8") as f:
            self.itens = json.load(f)
        with open("servidor/dados/inimigos.json", "r", encoding="utf-8") as f:
            self.inimigos = json.load(f)

    def registar_player(self, player: dict):
        with self.lock:
            if player not in self.jogadores:
                self.jogadores.append(player)
                self.nr_jogadores += 1
        print(self.jogadores)
    
    def get_players_info(self, players=None):
        with self.lock:
            if players is None:
                return self.jogadores.copy()
            else:
                return [p for p in self.jogadores if p["nome"] in players]