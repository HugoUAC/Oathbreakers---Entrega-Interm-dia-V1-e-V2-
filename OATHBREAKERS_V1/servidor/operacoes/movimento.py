class Movimento:
    def __init__(self, connection, address, s):
        self.connection = connection
        self.address = address
        self.s = s

    def move_up(self, player):
        player["posicao"][1] += 1

    def move_down(self, player):
        player["posicao"][1] -= 1

    def move_left(self, player):    
        player["posicao"][0] -= 1

    def move_right(self, player):
        player["posicao"][0] += 1
