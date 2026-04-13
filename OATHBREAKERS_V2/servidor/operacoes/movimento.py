class Movimento:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address

    def move_up(self, player):
        player["posicao"][1] += 1

    def move_down(self, player):
        player["posicao"][1] -= 1

    def move_left(self, player):
        player["posicao"][0] -= 1

    def move_right(self, player):
        player["posicao"][0] += 1
