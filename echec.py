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

    def clearDots(self,  moves: list = []):
        self.dotBoard = [[0 for i in range(8)] for j in range(8)]
        for move in moves:
            self.dotBoard[move[1]][move[0]] = 1


    def initiate(self, P1: str = "White", P2: str = "Black"):
        """
        Initiates the correct variables for a new game
        """
        self.p1 = P1
        self.p2 = P2
        self.gui = GUIechec()
        self.board = [['BR', 'BN', 'BB', 'BK', 'BQ', 'BB', 'BN', 'BR']] + [['BP' for i in range(8)]] + [[0 for i in range(8)] for j in range(4)] + [['WP' for i in range(8)]] + [['WR', 'WN', 'WB', 'WK', 'WQ', 'WB', 'WN', 'WR']]
        self.moves = []
        self.dotBoard = [[0 for i in range(8)] for j in range(8)]
        self.gui.refresh(self.board, "", self.dotBoard)
        self.white = True

    def customBoard(self, Board):
        self.board = Board

    def knight(self, inp):
        moves = [
            (inp[0]-2,inp[1]-1),
            (inp[0]-1,inp[1]-2),
            (inp[0]+2,inp[1]-1),
            (inp[0]+1,inp[1]-2),
            (inp[0]+2,inp[1]+1),
            (inp[0]+1,inp[1]+2),
            (inp[0]-2,inp[1]+1),
            (inp[0]-1,inp[1]+2)
        ]
        finalMoves = []
        for move in moves:
            if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                piece = self.board[move[1]][move[0]]
                if self.white:
                    if piece == 0 or piece == "BQ" or piece == "BR" or piece == "BB" or piece == "BN" or piece == "BP":
                        finalMoves.append(move)
                else:
                    if piece == 0 or piece == "WQ" or piece == "WR" or piece == "WB" or piece == "WN" or piece == "WP":
                        finalMoves.append(move)
        # print(moves)
        # print(finalMoves)
        return finalMoves

    def run(self):
        """
        Main running loop for the game
        """
        self.runs = True
        while self.runs:
            self.gui.refresh(self.board, "", self.dotBoard)
            inp = game.gui.waitClick()
            # print(inp)
            moves = []

            if self.white:
                if isinstance(inp, tuple):
                    if self.board[inp[1]][inp[0]] == "WK":
                        pass
                    elif self.board[inp[1]][inp[0]] == "WQ":
                        pass
                    elif self.board[inp[1]][inp[0]] == "WR":
                        pass
                    elif self.board[inp[1]][inp[0]] == "WB":
                        pass
                    elif self.board[inp[1]][inp[0]] == "WN":
                        moves = self.knight(inp)
                    elif self.board[inp[1]][inp[0]] == "WP":
                        pass

            if not self.white:
                if isinstance(inp, tuple):
                    if self.board[inp[1]][inp[0]] == "BK":
                        pass
                    elif self.board[inp[1]][inp[0]] == "BQ":
                        pass
                    elif self.board[inp[1]][inp[0]] == "BR":
                        pass
                    elif self.board[inp[1]][inp[0]] == "BB":
                        pass
                    elif self.board[inp[1]][inp[0]] == "BN":
                        moves = self.knight(inp)
                    elif self.board[inp[1]][inp[0]] == "BP":
                        pass

            if isinstance(inp, tuple):
                # print(self.board[inp[1]][inp[0]])
                self.clearDots(moves)


# -------------------------------- Main program ------------------------------- #

game = Game()
game.initiate()
# game.customBoard([['BR', 'WN', 'BB', 'BK', 'BQ', 'BB', 'BN', 'BR']] + [['BP' for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,"WN",0,0,0,0]] +  [[0 for i in range(8)] for j in range(2)] + [['WP' for i in range(8)]] + [['WR', 'WN', 'WB', 'WK', 'WQ', 'WB', 'WN', 'WR']])
game.run()