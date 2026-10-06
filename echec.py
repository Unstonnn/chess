from guiEchec import *

# ---------------------------------- Classes ---------------------------------- #

class Game():
    """
    Main chess game class.
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
        self.board = [[Rook(False), Knight(False), Bishop(False), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)] for j in range(4)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]]
        self.moves = []
        self.dotBoard = [[0 for i in range(8)] for j in range(8)]
        self.gui.refresh(self.formattedBoard(), "", self.dotBoard)
        self.white = True

    def formattedBoard(self):
        board = []
        for i in range(len(self.board)):
            board.append([])
            for square in self.board[i]:
                if square == 0:
                    board[i].append(0)
                elif isinstance(square,Rook):
                    if square.white:
                        board[i].append("WR")
                    else:
                        board[i].append("BR")
                elif isinstance(square,Knight):
                    if square.white:
                        board[i].append("WN")
                    else:
                        board[i].append("BN")
                elif isinstance(square,Bishop):
                    if square.white:
                        board[i].append("WB")
                    else:
                        board[i].append("BB")
                elif isinstance(square,King):
                    if square.white:
                        board[i].append("WK")
                    else:
                        board[i].append("BK")
                elif isinstance(square,Queen):
                    if square.white:
                        board[i].append("WQ")
                    else:
                        board[i].append("BQ")
                elif isinstance(square,Pawn):
                    if square.white:
                        board[i].append("WP")
                    else:
                        board[i].append("BP")
        return board

    def customBoard(self, Board):
        self.board = Board

    def run(self):
        """
        Main running loop for the game
        """
        self.runs = True
        while self.runs:
            self.gui.refresh(self.formattedBoard(), "", self.dotBoard)
            inp = self.gui.waitClick()
            # print(inp)
            moves = []

            if isinstance(inp, tuple):
                if self.board[inp[1]][inp[0]] == 0:
                    pass
                else:
                    moves = self.board[inp[1]][inp[0]].clicked(inp, self)

            if isinstance(inp, tuple):
                self.clearDots(moves)

class Knight():
    """
    Class for knight movement.
    Dependent on class GUIechec from guiEchec.
    """

    def __init__(self, White: bool):
        self.white = White

    def clicked(self, inp, Game):
        finalMoves = []
        if Game.white == self.white:
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
            for move in moves:
                if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                    piece = Game.board[move[1]][move[0]]
                    if piece == 0:
                        finalMoves.append(move)
                    elif piece.white != self.white:
                        finalMoves.append(move)
        return finalMoves

class Bishop():
    """
    Class for bishop movement.
    Dependent on class GUIechec from guiEchec.
    """

    def __init__(self, White: bool):
        self.white = White

    def clicked(self, inp, Game):
        moves = []
        if Game.white == self.white:
            for i in range(1,8):
                if inp[0]+i <= 7 and inp[1]+i <= 7 and inp[0]+i >= 0 and inp[1]+i >= 0:
                    if Game.board[inp[1]+i][inp[0]+i] == 0:
                        moves.append((inp[0]+i, inp[1]+i))
                    elif Game.board[inp[1]+i][inp[0]+i].white != self.white:
                        moves.append((inp[0]+i, inp[1]+i))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[0]-i <= 7 and inp[1]+i <= 7 and inp[0]-i >= 0 and inp[1]+i >= 0:
                    if Game.board[inp[1]+i][inp[0]-i] == 0:
                        moves.append((inp[0]-i, inp[1]+i))
                    elif Game.board[inp[1]+i][inp[0]-i].white != self.white:
                        moves.append((inp[0]-i, inp[1]+i))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[0]-i <= 7 and inp[1]-i <= 7 and inp[0]-i >= 0 and inp[1]-i >= 0:
                    if Game.board[inp[1]-i][inp[0]-i] == 0:
                        moves.append((inp[0]-i, inp[1]-i))
                    elif Game.board[inp[1]-i][inp[0]-i].white != self.white:
                        moves.append((inp[0]-i, inp[1]-i))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[0]+i <= 7 and inp[1]-i <= 7 and inp[0]+i >= 0 and inp[1]-i >= 0:
                    if Game.board[inp[1]-i][inp[0]+i] == 0:
                        moves.append((inp[0]+i, inp[1]-i))
                    elif Game.board[inp[1]-i][inp[0]+i].white != self.white:
                        moves.append((inp[0]+i, inp[1]-i))
                        break
                    else:
                        break

        return moves

class Rook():
    """
    Class for rook movement.
    Dependent on class GUIechec from guiEchec.
    """

    def __init__(self, White: bool):
        self.white = White

    def clicked(self, inp, Game):
        moves = []
        if Game.white == self.white:
            for i in range(1,8):
                if inp[0]+i <= 7 and inp[0]+i >= 0:
                    if Game.board[inp[1]][inp[0]+i] == 0:
                        moves.append((inp[0]+i, inp[1]))
                    elif Game.board[inp[1]][inp[0]+i].white != self.white:
                        moves.append((inp[0]+i, inp[1]))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[0]-i <= 7 and inp[0]-i >= 0:
                    if Game.board[inp[1]][inp[0]-i] == 0:
                        moves.append((inp[0]-i, inp[1]))
                    elif Game.board[inp[1]][inp[0]-i].white != self.white:
                        moves.append((inp[0]-i, inp[1]))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[1]-i <= 7 and inp[1]-i >= 0:
                    if Game.board[inp[1]-i][inp[0]] == 0:
                        moves.append((inp[0], inp[1]-i))
                    elif Game.board[inp[1]-i][inp[0]].white != self.white:
                        moves.append((inp[0], inp[1]-i))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[1]+i <= 7 and inp[1]+i >= 0:
                    if Game.board[inp[1]+i][inp[0]] == 0:
                        moves.append((inp[0], inp[1]+i))
                    elif Game.board[inp[1]+i][inp[0]].white != self.white:
                        moves.append((inp[0], inp[1]+i))
                        break
                    else:
                        break

        return moves

class King():
    """
    Class for king movement.
    Dependent on class GUIechec from guiEchec.
    """

    def __init__(self, White: bool):
        self.white = White

    def clicked(self, inp, Game):
        finalMoves = []
        if Game.white == self.white:
            moves = [
                (inp[0]-1,inp[1]-1),
                (inp[0]-1,inp[1]),
                (inp[0]+1,inp[1]-1),
                (inp[0]+1,inp[1]),
                (inp[0]+1,inp[1]+1),
                (inp[0],inp[1]+1),
                (inp[0]-1,inp[1]+1),
                (inp[0],inp[1]+1)
            ]
            for move in moves:
                if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                    piece = Game.board[move[1]][move[0]]
                    if piece == 0:
                        finalMoves.append(move)
                    elif piece.white != self.white:
                        finalMoves.append(move)
        return finalMoves

class Queen():
    """
    Class for queen movement.
    Dependent on class GUIechec from guiEchec.
    """

    def __init__(self, White: bool):
        self.white = White

    def clicked(self, inp, Game):
        moves = []
        if Game.white == self.white:
            for i in range(1,8):
                if inp[0]+i <= 7 and inp[1]+i <= 7 and inp[0]+i >= 0 and inp[1]+i >= 0:
                    if Game.board[inp[1]+i][inp[0]+i] == 0:
                        moves.append((inp[0]+i, inp[1]+i))
                    elif Game.board[inp[1]+i][inp[0]+i].white != self.white:
                        moves.append((inp[0]+i, inp[1]+i))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[0]-i <= 7 and inp[1]+i <= 7 and inp[0]-i >= 0 and inp[1]+i >= 0:
                    if Game.board[inp[1]+i][inp[0]-i] == 0:
                        moves.append((inp[0]-i, inp[1]+i))
                    elif Game.board[inp[1]+i][inp[0]-i].white != self.white:
                        moves.append((inp[0]-i, inp[1]+i))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[0]-i <= 7 and inp[1]-i <= 7 and inp[0]-i >= 0 and inp[1]-i >= 0:
                    if Game.board[inp[1]-i][inp[0]-i] == 0:
                        moves.append((inp[0]-i, inp[1]-i))
                    elif Game.board[inp[1]-i][inp[0]-i].white != self.white:
                        moves.append((inp[0]-i, inp[1]-i))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[0]+i <= 7 and inp[1]-i <= 7 and inp[0]+i >= 0 and inp[1]-i >= 0:
                    if Game.board[inp[1]-i][inp[0]+i] == 0:
                        moves.append((inp[0]+i, inp[1]-i))
                    elif Game.board[inp[1]-i][inp[0]+i].white != self.white:
                        moves.append((inp[0]+i, inp[1]-i))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[0]+i <= 7 and inp[0]+i >= 0:
                    if Game.board[inp[1]][inp[0]+i] == 0:
                        moves.append((inp[0]+i, inp[1]))
                    elif Game.board[inp[1]][inp[0]+i].white != self.white:
                        moves.append((inp[0]+i, inp[1]))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[0]-i <= 7 and inp[0]-i >= 0:
                    if Game.board[inp[1]][inp[0]-i] == 0:
                        moves.append((inp[0]-i, inp[1]))
                    elif Game.board[inp[1]][inp[0]-i].white != self.white:
                        moves.append((inp[0]-i, inp[1]))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[1]-i <= 7 and inp[1]-i >= 0:
                    if Game.board[inp[1]-i][inp[0]] == 0:
                        moves.append((inp[0], inp[1]-i))
                    elif Game.board[inp[1]-i][inp[0]].white != self.white:
                        moves.append((inp[0], inp[1]-i))
                        break
                    else:
                        break

            for i in range(1,8):
                if inp[1]+i <= 7 and inp[1]+i >= 0:
                    if Game.board[inp[1]+i][inp[0]] == 0:
                        moves.append((inp[0], inp[1]+i))
                    elif Game.board[inp[1]+i][inp[0]].white != self.white:
                        moves.append((inp[0], inp[1]+i))
                        break
                    else:
                        break
        return moves

class Pawn():
    """
    Class for pawn movement.
    Dependent on class GUIechec from guiEchec.
    """

    def __init__(self, White: bool):
        self.white = White
        self.moved = False

    def clicked(self, inp, Game): # haven't done en passant cause needs Game.moves != []
        if Game.white == self.white: # also haven't added promotion
            mult = 1
            if self.white:
                mult = -1 # moves -1 if white but 1 if white
            moves = []
            piece = Game.board[inp[1]+mult*1][inp[0]]
            if piece == 0:
                moves.append((inp[0], inp[1]+mult*1))
            piece = Game.board[inp[1]+mult*2][inp[0]]
            if not self.moved and piece == 0:
                moves.append((inp[0], inp[1]+mult*2))
            if inp[0]+1 <= 7:
                piece = Game.board[inp[1]+mult*1][inp[0]+1]
                if piece != 0:
                    if piece.white != self.white:
                        moves.append((inp[0]+1, inp[1]+mult*1))
            if inp[0]-1 >= 0:
                piece = Game.board[inp[1]+mult*1][inp[0]-1]
                if piece != 0:
                    if piece.white != self.white:
                        moves.append((inp[0]-1, inp[1]+mult*1))
        return moves
            

# -------------------------------- Main program ------------------------------- #

game = Game()
game.initiate()
# game.customBoard([[Rook(False), Knight(True), Bishop(False), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,Knight(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
# game.customBoard([[Rook(False), Knight(False), Bishop(False), King(True), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,King(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
# game.customBoard([[Rook(False), Knight(False), Bishop(True), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,Bishop(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
# game.customBoard([[Rook(True), Knight(False), Bishop(False), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,Rook(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
# Sgame.customBoard([[Rook(False), Knight(False), Bishop(False), King(False), Queen(True), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,Queen(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
game.customBoard([[Rook(False), Knight(False), Bishop(False), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[Pawn(True),0,0,Pawn(True),0,0,0,Pawn(True)]] + [[0,0,Pawn(True),0,0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
game.run()