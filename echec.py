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
        attacks = []
        for i, row in enumerate(self.board):
            for j, piece in enumerate(row):
                inp = (j,i)
                if piece != 0:
                    if not piece.white == self.white:
                        moves, _ = piece.clicked(inp, self, True)
                        attacks.extend(moves)
                    elif isinstance(piece,King):
                        king = inp
        for attack in attacks:
            if attack == king:
                return True
        return False

    def win(self, reason): # Ways to win: Checkmate ; resignation ; time
        self.runs = False
        color = "Black" if self.white else "White"
        if reason == 0:
            reason = "By checkmate"
        elif reason == 1:
            reason = "By resignation"
        elif reason == 2:
            reason = "On time"
        self.gui.refresh(self.formattedBoard(), reason, self.dotBoard)
        self.gui.messCentre(f"{color} wins")

    def draw(self, reason): # Ways to draw: No moves ; insufficient material ; repetition ; 50 moves ; stalemate ; agreement
        self.runs = False
        if reason == 0:
            reason = "By stalemate"
        elif reason == 1:
            reason = "By agreement"
        elif reason == 2:
            reason = "By repetition"
        elif reason == 3:
            reason = "By insufficient material"
        elif reason == 4:
            reason = "By the 50-move rule"
        self.gui.refresh(self.formattedBoard(), reason, self.dotBoard)
        self.gui.messCentre("Draw")

    def filteredMoves(self, moves, piece):
        finalMoves = []
        for move in moves:
            actPiece = self.board[piece[1]][piece[0]]
            if len(move) == 3: #castling
                inCheck = False
                if self.isInCheck():
                    inCheck = True
                self.board[move[1][1]][move[1][0]] = actPiece # moves king
                self.board[piece[1]][piece[0]] = 0
                if not inCheck and self.isInCheck():
                    inCheck = True
                self.board[move[0][1]][move[0][0]] = self.board[move[1][1]][move[1][0]] # moves king
                self.board[move[1][1]][move[1][0]] = self.board[move[2][1]][move[2][0]] # moves rook
                self.board[move[2][1]][move[2][0]] = 0
                if not self.isInCheck() and not inCheck:
                    finalMoves.append(move)
                self.board[piece[1]][piece[0]] = self.board[move[0][1]][move[0][0]]
                self.board[move[0][1]][move[0][0]] = 0
                self.board[move[2][1]][move[2][0]] = self.board[move[1][1]][move[1][0]]
                self.board[move[1][1]][move[1][0]] = 0
                continue
            if isinstance(move[0], tuple):
                finalMoves.append(move)
                continue
            actMove = self.board[move[1]][move[0]]
            self.board[move[1]][move[0]] = self.board[piece[1]][piece[0]]
            self.board[piece[1]][piece[0]] = 0
            if not self.isInCheck():
                finalMoves.append(move)
            self.board[move[1]][move[0]] = actMove
            self.board[piece[1]][piece[0]] = actPiece
        return finalMoves

    def run(self):
        """
        Main running loop for the game
        """
        self.runs = True
        moves = []
        moveRule = 0 # 50-move rule counter
        while self.runs:
            toSkip = False
            self.gui.refresh(self.formattedBoard(), "", self.dotBoard)

            allMoves = [] # checks for game end conditions
            selfPieces = []
            selfIF = []
            otherPieces = []
            otherIF = []
            for i, row in enumerate(self.board):
                for j, square in enumerate(row):
                    if square != 0:
                        if square.white == self.white:
                            pieceMoves, boardPiece = square.clicked((j,i), self)
                            pieceMoves = self.filteredMoves(pieceMoves, boardPiece)
                            allMoves.extend(pieceMoves)
                            selfPieces.append(self.board[j][i])
                            if isinstance(square, King) or isinstance(square, Knight) or isinstance(square, Bishop):
                                selfIF.append(self.board[j][i])
                        else:
                            otherPieces.append(self.board[j][i])
                            if isinstance(square, King) or isinstance(square, Knight) or isinstance(square, Bishop):
                                otherIF.append(self.board[j][i])
            if allMoves == []:
                if self.isInCheck():
                    self.win(0) # Checkmate
                else:
                    self.draw(0) # Stalemate
            if len(selfIF) <= 2 and len(otherIF) <= 2 and selfPieces == selfIF and otherPieces == otherIF:
                self.draw(3) # Insufficient material
            repetition = 0
            for state in self.moves:
                if state == self.board:
                    repetition += 1
            if repetition == 3:
                self.draw(2) # Repetition
            if moveRule >= 50:
                self.draw(4) # 50-move rule
            print(moveRule)
            
            inp = self.gui.waitClick()
            # print(inp)

            if moves != []:
                for move in moves:
                    if isinstance(move[0],tuple): # en passant logic
                        if move[0] == inp and isinstance(self.board[piece[1]][piece[0]], Pawn):
                            self.board[inp[1]][inp[0]] = self.board[piece[1]][piece[0]]
                            self.board[piece[1]][piece[0]] = 0
                            self.board[move[1][1]][move[1][0]] = 0
                            moveRule = 0
                            self.reverse()
                            self.moves.append([row.copy() for row in self.board])
                            toSkip = True
                            # print(self.isInCheck())
                            break
                        elif move[0] == inp and isinstance(self.board[piece[1]][piece[0]], King): # castling logic
                            self.board[inp[1]][inp[0]] = self.board[piece[1]][piece[0]]
                            self.board[piece[1]][piece[0]] = 0
                            self.board[move[1][1]][move[1][0]] = self.board[move[2][1]][move[2][0]]
                            self.board[move[2][1]][move[2][0]] = 0
                            self.board[inp[1]][inp[0]].moved = True
                            self.board[move[1][1]][move[1][0]].moved = True
                            moveRule += 1
                            self.reverse()
                            self.moves.append([row.copy() for row in self.board])
                            toSkip = True
                            # print(self.isInCheck())
                            break
                    if move == inp:
                        self.board[inp[1]][inp[0]] = self.board[piece[1]][piece[0]]
                        self.board[piece[1]][piece[0]] = 0
                        if inp[1] == 0 and isinstance(self.board[inp[1]][inp[0]], Pawn):
                            self.board[inp[1]][inp[0]] = Queen(self.white)
                        elif isinstance(self.board[inp[1]][inp[0]], King):
                            self.board[inp[1]][inp[0]].moved = True
                        elif isinstance(self.board[inp[1]][inp[0]], Rook):
                            self.board[inp[1]][inp[0]].moved = True
                        if self.moves[-1][inp[1]][inp[0]] != 0 or isinstance(self.board[inp[1]][inp[0]], Pawn):
                            moveRule = 0
                        else:
                            moveRule += 1
                        self.reverse()
                        self.moves.append([row.copy() for row in self.board])
                        toSkip = True
                        # print(self.isInCheck())
                        break

            moves = []
            self.clearDots()
            if not toSkip:
                if isinstance(inp, tuple):
                    if self.board[inp[1]][inp[0]] == 0:
                        pass
                    else:
                        moves, piece = self.board[inp[1]][inp[0]].clicked(inp, self)
                        moves = self.filteredMoves(moves, piece)
                self.clearDots(moves)

class Knight():
    """
    Class for knight movement.
    Dependent on class GUIechec from guiEchec.
    """

    def __init__(self, White: bool):
        self.white = White

    def clicked(self, inp, Game, check: bool = False):
        finalMoves = []
        if Game.white == self.white or check:
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

    def clicked(self, inp, Game, check: bool = False):
        moves = []
        if Game.white == self.white or check:
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
        self.moved = False

    def clicked(self, inp, Game, check: bool = False):
        moves = []
        if Game.white == self.white or check:
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
        self.moved = False

    def clicked(self, inp, Game, check: bool = False):
        finalMoves = []
        if Game.white == self.white or check:
            moves = [
                (inp[0]-1,inp[1]-1),
                (inp[0]-1,inp[1]),
                (inp[0]+1,inp[1]-1),
                (inp[0]+1,inp[1]),
                (inp[0]+1,inp[1]+1),
                (inp[0],inp[1]+1),
                (inp[0]-1,inp[1]+1),
                (inp[0],inp[1]-1)
            ]
            for move in moves:
                if move[0] >= 0 and move[0] <= 7 and move[1] >= 0 and move[1] <= 7:
                    piece = Game.board[move[1]][move[0]]
                    if piece == 0:
                        finalMoves.append(move)
                    elif piece.white != self.white:
                        finalMoves.append(move)

            if not self.moved: # Castling
                if isinstance(Game.board[7][0], Rook) and not Game.board[7][0].moved:
                    empty = True
                    for i in range(1,inp[0]):
                        if Game.board[7][i] != 0:
                            empty = False
                    if empty:
                        finalMoves.append(((inp[0]-2,inp[1]),(inp[0]-1,inp[1]),(0,7)))
                if isinstance(Game.board[7][7], Rook) and not Game.board[7][7].moved:
                    empty = True
                    for i in range(inp[0]+1,7):
                        if Game.board[7][i] != 0:
                            empty = False
                    if empty:
                        finalMoves.append(((inp[0]+2,inp[1]),(inp[0]+1,inp[1]),(7,7)))
        return finalMoves, inp

class Queen():
    """
    Class for queen movement.
    Dependent on class GUIechec from guiEchec.
    """

    def __init__(self, White: bool):
        self.white = White

    def clicked(self, inp, Game, check: bool = False):
        moves = []
        if Game.white == self.white or check:
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

    def clicked(self, inp, Game, check: bool = False):
        moves = []
        if check:
            if inp[0]+1 <= 7:
                piece = Game.board[inp[1]+1][inp[0]+1]
                if piece != 0:
                    if piece.white != self.white:
                        moves.append((inp[0]+1, inp[1]+1))
            if inp[0]-1 >= 0:
                piece = Game.board[inp[1]+1][inp[0]-1]
                if piece != 0:
                    if piece.white != self.white:
                        moves.append((inp[0]-1, inp[1]+1))
            return moves, inp
                
        if Game.white == self.white: # also haven't added manual promotion
            piece = Game.board[inp[1]-1][inp[0]]
            if piece == 0:
                moves.append((inp[0], inp[1]-1))
            piece = Game.board[inp[1]-2][inp[0]]
            if inp[1] == 6 and piece == 0:
                moves.append((inp[0], inp[1]-2))
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

while True:
    inp = input()

    game = Game()
    game.initiate()
    # game.customBoard([[Rook(False), Knight(True), Bishop(False), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,Knight(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
    # game.customBoard([[Rook(False), Knight(False), Bishop(False), King(True), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,King(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
    # game.customBoard([[Rook(False), Knight(False), Bishop(True), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,Bishop(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
    # game.customBoard([[Rook(True), Knight(False), Bishop(False), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,Rook(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
    # game.customBoard([[Rook(False), Knight(False), Bishop(False), King(False), Queen(True), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,Queen(True),0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
    # game.customBoard([[Rook(False), Knight(False), Bishop(False), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[Pawn(True),0,0,Pawn(True),0,0,0,Pawn(True)]] + [[0,0,Pawn(True),0,0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
    # game.customBoard([[0, 0, 0, King(False), 0, 0, 0, 0]] + [[0 for i in range(8)] for j in range(6)] + [[0, 0, 0, King(True), Queen(True), 0, 0, 0]])
    game.run()