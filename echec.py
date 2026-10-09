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
        self.board = [list(reversed(row)) for row in self.board]

    def clearDots(self,  moves: list = []):
        self.dotBoard = [[0 for i in range(8)] for j in range(8)]
        for move in moves:
            if isinstance(move[0], tuple):
                self.dotBoard[move[0][1]][move[0][0]] = 1
            else:
                self.dotBoard[move[1]][move[0]] = 1

    def initiate(self, P1: str = "White", P2: str = "Black"):
        """
        Initiates the correct variables for a new game
        """
        self.p1 = P1
        self.p2 = P2
        self.gui = GUIechec()
        self.board = [[Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)] for j in range(4)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), Queen(True), King(True), Bishop(True), Knight(True), Rook(True)]]
        self.moves = [[row.copy() for row in self.board]]
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

    def isInCheck(self):
        for row in self.board:
            for square in row:
                if square != 0:
                    if not square.white == self.white:
                        pass # building this rn

    def run(self):
        """
        Main running loop for the game
        """
        self.runs = True
        moves = []
        while self.runs:
            self.gui.refresh(self.formattedBoard(), "", self.dotBoard)
            inp = self.gui.waitClick()
            # print(inp)
            
            if moves != []:
                for move in moves:
                    if isinstance(move[0],tuple): # en passant logic
                        if move[0] == inp:
                            self.board[inp[1]][inp[0]] = self.board[piece[1]][piece[0]]
                            self.board[piece[1]][piece[0]] = 0
                            self.board[move[1][1]][move[0][0]] = 0
                            self.reverse()
                            self.moves.append([row.copy() for row in self.board])
                            break
                    if move == inp:
                        self.board[inp[1]][inp[0]] = self.board[piece[1]][piece[0]]
                        self.board[piece[1]][piece[0]] = 0
                        if inp[1] == 0 and isinstance(self.board[inp[1]][inp[0]], Pawn):
                            self.board[inp[1]][inp[0]] = Queen(self.white)
                        self.reverse()
                        self.moves.append([row.copy() for row in self.board])
                        break

            moves = []
            if isinstance(inp, tuple):
                if self.board[inp[1]][inp[0]] == 0:
                    pass
                else:
                    moves, piece = self.board[inp[1]][inp[0]].clicked(inp, self)

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
        return finalMoves, inp

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

        return moves, inp

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

        return moves, inp

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
        return finalMoves, inp

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
        return moves, inp

class Pawn():
    """
    Class for pawn movement.
    Dependent on class GUIechec from guiEchec.
    """

    def __init__(self, White: bool):
        self.white = White
        self.moved = False

    def clicked(self, inp, Game):
        moves = []
        if Game.white == self.white: # also haven't added manual promotion
            piece = Game.board[inp[1]-1][inp[0]]
            if piece == 0:
                moves.append((inp[0], inp[1]-1))
            piece = Game.board[inp[1]-2][inp[0]]
            if not self.moved and piece == 0:
                moves.append((inp[0], inp[1]-2))
                self.moved = True
            if inp[0]+1 <= 7:
                piece = Game.board[inp[1]-1][inp[0]+1]
                if piece != 0:
                    if piece.white != self.white:
                        moves.append((inp[0]+1, inp[1]-1))
            if inp[0]-1 >= 0:
                piece = Game.board[inp[1]-1][inp[0]-1]
                if piece != 0:
                    if piece.white != self.white:
                        moves.append((inp[0]-1, inp[1]-1))
            if inp[1] == 3: # en passant
                if inp[0]-1 >= 0 and len(Game.moves) >= 2:
                    piece = Game.board[inp[1]][inp[0]-1]
                    if isinstance(Game.moves[-2][inp[1]-2][inp[0]-1], Pawn) and Game.moves[-1][inp[1]-2][inp[0]-1] == 0 and isinstance(Game.moves[-1][inp[1]][inp[0]-1], Pawn):
                        moves.append(((inp[0]-1,inp[1]-1),(inp[0]-1,inp[1])))
                if inp[0]-1 <= 7:
                    piece = Game.board[inp[1]][inp[0]+1]
                    if isinstance(Game.moves[-2][inp[1]-2][inp[0]+1], Pawn) and Game.moves[-1][inp[1]-2][inp[0]+1] == 0 and isinstance(Game.moves[-1][inp[1]][inp[0]+1], Pawn):
                        moves.append(((inp[0]+1,inp[1]-1),(inp[0]+1,inp[1])))
                
        return moves, inp

# -------------------------------- Main program ------------------------------- #

game = Game()
game.initiate()
# game.customBoard([[Rook(False), Knight(True), Bishop(False), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,Knight(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
# game.customBoard([[Rook(False), Knight(False), Bishop(False), King(True), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,King(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
# game.customBoard([[Rook(False), Knight(False), Bishop(True), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,Bishop(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
# game.customBoard([[Rook(True), Knight(False), Bishop(False), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,Rook(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
# game.customBoard([[Rook(False), Knight(False), Bishop(False), King(False), Queen(True), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,Queen(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
# game.customBoard([[Rook(False), Knight(False), Bishop(False), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[Pawn(True),0,0,Pawn(True),0,0,0,Pawn(True)]] + [[0,0,Pawn(True),0,0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
game.run()