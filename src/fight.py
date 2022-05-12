class Fight:
    def __init__(self, id):
        self.id = id
        self.ready = False
        self.result = [None, None]
        self.winner = None

    def take_winner(self):
        if self.result[0] > self.result[1]:
            self.winner = 0
        else:
            self.winner = 1


