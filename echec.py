from guiEchec import *

# ---------------------------------- Classes ---------------------------------- #

class Game():
    """
    Class to chess games.
    Dependent on class GUIechec from guiEchec.
    """

    def __init__(self):
        pass # after will fill when doing menu

    def reverse(self):
        self.white = not self.white
        self.gui.flipNum = self.white
        self.board = list(reversed(self.board))

    def game(self, P1: str = "White", P2: str = "Black"):
        """
        Starts a game
        """
        self.p1 = P1
        self.p2 = P2
        self.gui = GUIechec()
        self.board = [['BR', 'BN', 'BB', 'BK', 'BQ', 'BB', 'BN', 'BR']] + [['BP' for i in range(8)]] + [[0 for i in range(8)] for j in range(4)] + [['WP' for i in range(8)]] + [['WR', 'WN', 'WB', 'WK', 'WQ', 'WB', 'WN', 'WR']]
        self.moves = []
        self.gui.refresh(self.board)
        self.white = False

        while True :
            self.gui.refresh(self.board)
            inp = game.gui.waitClick()
            print(inp)
            if isinstance(inp, tuple):
                print(self.board[inp[1]][inp[0]])
                self.reverse()

# -------------------------------- Main program ------------------------------- #

game = Game()
game.game()