from guiEchec import *
from time import monotonic
import random

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# cspell:ignore Stockfish, Singleplayer

# ---------------------------------- Classes ---------------------------------- #

class Game:
    """Manage a chess game, its board state, rules, timer, and GUI."""

    def __init__(self, skip = False, board = None):
        """Create a game and start the menu or the game loop.

        Args:
            skip: Start directly without displaying the interactive menu.
            board: Optional initial board used in place of the standard setup.
        """
        self.autoPromote = True
        self.timer = False
        self.baseTime = 15
        self.increment = 10
        self.playStockfish = False
        self.showAnalysis = False
        mainMenu = True
        mainOptions = True
        skillLevel = "Medium"
        self.playingWhite = True
        playedColor = "Random"
        colorEnum = {"Random": "White", "White": "Black", "Black": "Random"}
        GRAY = '\033[90m'
        RED  = '\033[91m'

        try:
            import inquirer
        except:
            print("Warning: Couldn't import inquirer")
            skip = True
        try:
            import ctypes
        except:
            skip = True
            print("Warning: Couldn't import ctypes")
        try:
            from stockfish import Stockfish
            self.stockfish = Stockfish(path="stockfish/stockfish-windows-x86-64-universal.exe")
            self.stockfish.set_skill_level(5)
            hasStockfish = True
        except:
            hasStockfish = False
            input("Warning: Couldn't import stockfish")
        while True:
            if skip:
                self.initiate()
                if board is not None:
                    self.customBoard(board)
                self.run()
            else:
                # startGame() built with the help of AI
                kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
                user32 = ctypes.WinDLL("user32", use_last_error=True)
                kernel32.GetConsoleWindow.restype = ctypes.wintypes.HWND
                user32.ShowWindow.argtypes = (ctypes.wintypes.HWND, ctypes.c_int)
                user32.SetForegroundWindow.argtypes = (ctypes.wintypes.HWND,)

                def focusWindow(hwnd):
                    """Bring a valid Windows window to the foreground."""
                    if hwnd:
                        user32.ShowWindow(hwnd, 5)
                        user32.SetForegroundWindow(hwnd)

                def startGame():
                    """Initialize and run a game, restoring the console afterward."""
                    self.initiate()
                    if board is not None:
                        self.customBoard(board)
                    console_hwnd = kernel32.GetConsoleWindow()
                    board_hwnd = pygame.display.get_wm_info().get("window")
                    try:
                        if console_hwnd:
                            user32.ShowWindow(console_hwnd, 0)
                        focusWindow(board_hwnd)
                        self.run()
                    finally:
                        pygame.quit()
                        if console_hwnd:
                            focusWindow(console_hwnd)

                if mainMenu:
                    questions = [
                    inquirer.List("choice", message=f"\033[2J\033[H{RED}Chess",
                                choices=["Start Game", "Options", "Quit"],
                                default="Start Game",
                                carousel=True)
                                ]
                    answers = inquirer.prompt(questions)
                    if answers["choice"] == "Start Game":
                        if hasStockfish:
                            questions = [
                            inquirer.List("choice", message=f"\033[2J\033[H{RED}Select Game Mode",
                                        choices=["Singleplayer", "Local Multiplayer", "Back"],
                                        carousel=True)
                                        ]
                            answers = inquirer.prompt(questions)
                            if answers["choice"] == "Singleplayer":
                                if playedColor == "White":
                                    self.playingWhite = True
                                elif playedColor == "Black":
                                    self.playingWhite = False
                                else:
                                    self.playingWhite = random.choice([True, False])
                                self.playStockfish = True
                                startGame()
                            elif answers["choice"] == "Local Multiplayer":
                                self.playStockfish = False
                                startGame()
                        else:
                            startGame()
                    elif answers["choice"] == "Options":
                        mainMenu = False
                    elif answers["choice"] == "Quit":
                        break
                else:
                    if mainOptions:
                        if not self.timer:
                            options = [f"Auto Promotion — {self.autoPromote}",
                                    f"Timer — {self.timer}",
                                    f"{GRAY}Starting Time — {self.baseTime}",
                                    f"{GRAY}Increment — {self.increment}"]
                        else:
                            options = [f"Auto Promotion — {self.autoPromote}",
                                    f"Timer — {self.timer}",
                                    f"Starting Time — {self.baseTime}",
                                    f"Increment — {self.increment}"]
                        if hasStockfish:
                            options.append("Singleplayer Options")
                        options.append("Back")
                        questions = [
                        inquirer.List("choice", message=f"\033[2J\033[H{RED}Options",
                                    choices=options,
                                    carousel=True)
                                    ]
                        answers = inquirer.prompt(questions)
                        if answers["choice"] == "Back":
                            mainMenu = True
                        elif answers["choice"] == options[0]:
                            self.autoPromote = not self.autoPromote
                        elif answers["choice"] == options[1]:
                            self.timer = not self.timer
                        elif self.timer:
                            if answers["choice"] == options[2]:
                                inp = input("\033[2J\033[HStarting Time (in minutes): ")
                                try:
                                    inp = int(inp)
                                    if inp > 0 and inp <= 720:
                                        self.baseTime = inp
                                    else:
                                        input("Number out of range")
                                except:
                                    input("Please enter an integer")
                            elif answers["choice"] == options[3]:
                                inp = input("\033[2J\033[HIncrement (in seconds): ")
                                try:
                                    inp = int(inp)
                                    if inp >= 0 and inp <= 240:
                                        self.increment = inp
                                    else:
                                        input("Number out of range")
                                except:
                                    input("Please enter an integer")
                        elif answers["choice"] == "Singleplayer Options":
                            mainOptions = False
                    else:
                        bestMove = f"Analysis — {self.showAnalysis}"
                        chosenColor = f"Color played — {playedColor}"
                        questions = [
                        inquirer.List("choice", message=f"\033[2J\033[H{RED}Singleplayer Options",
                                    choices=["Difficulty", chosenColor, bestMove, "Back"],
                                    carousel=True)
                                    ]
                        answers = inquirer.prompt(questions)
                        if answers["choice"] == "Back":
                            mainOptions = True
                        elif answers["choice"] == bestMove:
                            self.showAnalysis = not self.showAnalysis
                        elif answers["choice"] == chosenColor:
                            playedColor = colorEnum[playedColor]
                        elif answers["choice"] == "Difficulty":
                            questions = [
                            inquirer.List("choice", message=f"\033[2J\033[H{RED}Difficulty",
                                        choices=["Easy", "Medium", "Hard", "Impossible", "Other", "Back"],
                                        default=skillLevel,
                                        carousel=True)
                                        ]
                            answers = inquirer.prompt(questions)
                            if answers["choice"] != "Back":
                                skillLevel = answers["choice"]
                            if answers["choice"] == "Easy":
                                self.stockfish.set_skill_level(1)
                            elif answers["choice"] == "Medium":
                                self.stockfish.set_skill_level(5)
                            elif answers["choice"] == "Hard":
                                self.stockfish.set_skill_level(13)
                            elif answers["choice"] == "Impossible":
                                self.stockfish.resume_full_strength()
                            elif answers["choice"] == "Other":
                                inp = input("\033[2J\033[HSkill Level (1-20): ")
                                try:
                                    inp = int(inp)
                                    if inp >= 1 and inp <= 20:
                                        self.stockfish.set_skill_level(inp)
                                    else:
                                        input("Number out of range")
                                except:
                                    input("Please enter an integer")

    def manualPromotion(self):
        """Ask the player to choose a piece when a pawn is promoted."""
        self.gui.refresh(self.formattedBoard(), "Promotion — Q | R | B | N")
        choices = {"Q": Queen, "R": Rook, "B": Bishop, "N": Knight}

        while True:
            choice = self.gui.waitClick()
            if isinstance(choice, str) and choice.upper() in choices:
                return choices[choice.upper()](self.white)

    def reversedBoard(self, board = None):
        if board is None:
            board = self.board
        actBoard = [row.copy() for row in board]
        actBoard = list(reversed(actBoard))
        actBoard = [list(reversed(row)) for row in actBoard]
        return actBoard

    def reverse(self):
        """Switch the active player and rotate the board for that player's view."""
        if self.timer and not self.playStockfish:
            self.remainingTime[self.white] -= monotonic() - self.turnStarted
            self.remainingTime[self.white] += self.increment
            self.turnStarted = monotonic()
        self.white = not self.white
        self.gui.flipNum = not self.white
        self.board = list(reversed(self.board))
        self.board = [list(reversed(row)) for row in self.board]
        if self.white:
            self.fullMoves += 1

    def clearDots(self,  moves: list = []):
        """Clear highlighted squares, then mark the supplied legal moves."""
        self.dotBoard = [[0 for i in range(8)] for j in range(8)]
        for move in moves:
            # Special moves store their destination inside the first tuple.
            if isinstance(move[0], tuple):
                self.dotBoard[move[0][1]][move[0][0]] = 1
            else:
                self.dotBoard[move[1]][move[0]] = 1

    def initiate(self, P1: str = "White", P2: str = "Black"):
        """Set up a standard chess position and initialize game state."""
        self.p1 = P1
        self.p2 = P2
        self.gui = GUIechec()
        self.board = [[Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)] for j in range(4)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), Queen(True), King(True), Bishop(True), Knight(True), Rook(True)]]
        # Keep a board snapshot so previous positions can be displayed and compared.
        self.moves = [[row.copy() for row in self.board]]
        self.dotBoard = [[0 for i in range(8)] for j in range(8)]
        self.gui.refresh(self.formattedBoard(), "", self.dotBoard)
        self.white = True
        self.halfMoves = 0 # 50-move rule counter
        self.fullMoves = 1
        if self.timer and not self.playStockfish:
            self.remainingTime = {True: self.baseTime * 60, False: self.baseTime * 60}

    def formattedBoard(self, actBoard = None):
        """Convert piece objects into the string codes expected by the GUI."""
        board = []
        if actBoard is None:
            actBoard = self.board
        for i in range(len(actBoard)):
            board.append([])
            for square in actBoard[i]:
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
        """Replace the current position with the supplied board."""
        self.board = Board

    def isInCheck(self):
        """Return whether the current player's king is attacked."""
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
        """End the game and display the winner and the reason."""
        self.runs = False
        color = "Black" if self.white else "White"
        if reason == 0:
            reason = "By checkmate"
        elif reason == 1:
            reason = "On time"
        self.gui.refresh(self.formattedBoard(), reason, self.dotBoard)
        self.gui.messCentre(f"{color} wins")

    def draw(self, reason): # Ways to draw: Insufficient material ; repetition ; 50 moves ; stalemate ; agreement
        """End the game and display a draw with the supplied reason."""
        self.runs = False
        if reason == 0:
            reason = "By stalemate"
        elif reason == 1:
            reason = "On time by insufficient material"
        elif reason == 2:
            reason = "By repetition"
        elif reason == 3:
            reason = "By insufficient material"
        elif reason == 4:
            reason = "By the 50-move rule"
        self.gui.refresh(self.formattedBoard(), reason, self.dotBoard)
        self.gui.messCentre("Draw")

    def filteredMoves(self, moves, piece):
        """Remove moves that leave the moving player's king in check."""
        finalMoves = []
        for move in moves:
            actPiece = self.board[piece[1]][piece[0]]
            if len(move) == 3: #castling
                # Test the king's starting, transit, and destination squares.
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
                # En passant is represented specially and checked by the move handler.
                finalMoves.append(move)
                continue
            # Temporarily apply each ordinary move to test for check, then restore it.
            actMove = self.board[move[1]][move[0]]
            self.board[move[1]][move[0]] = self.board[piece[1]][piece[0]]
            self.board[piece[1]][piece[0]] = 0
            if not self.isInCheck():
                finalMoves.append(move)
            self.board[move[1]][move[0]] = actMove
            self.board[piece[1]][piece[0]] = actPiece
        return finalMoves

    def formatTime(self):
        """Return the active player's remaining time as a display string."""
        self.elapsedTime = monotonic() - self.turnStarted
        timeLeft = self.remainingTime[self.white] - self.elapsedTime
        centiSecondsLeft = max(0, int(timeLeft * 100))
        minutes, remainder = divmod(centiSecondsLeft, 6000)
        seconds, centiSeconds = divmod(remainder, 100)
        if minutes:
            return f"{minutes}:{seconds:02}.{centiSeconds:02}"
        return f"{seconds}.{centiSeconds:02}"

    def previousMoves(self):
        """Let the player browse earlier board snapshots until they exit."""
        allTurns = len(self.moves)
        turnsBack = 2
        if turnsBack > allTurns:
            return
        while True:
            if self.timer and not self.playStockfish:
                text = self.formatTime()
            else:
                text = ""
            if turnsBack % 2 == 0:
                self.gui.refresh(self.formattedBoard(self.reversedBoard(self.moves[-turnsBack])), text)
            else:
                self.gui.refresh(self.formattedBoard(self.moves[-turnsBack]), text)


            if self.timer and not self.playStockfish:
                inp = self.gui.waitClick(monotonic())
            else:
                inp = self.gui.waitClick()

            if inp == '_L':
                turnsBack += 1
            elif inp == '_R':
                turnsBack -= 1
            elif inp == "_T":
                continue
            else:
                return

            if turnsBack == 1:
                return
            if turnsBack > allTurns:
                turnsBack = allTurns

    def formatFEN(self, enPassant='-'):
        pieceMap = {
        'BR': 'r', 'BN': 'n', 'BB': 'b', 'BQ': 'q', 'BK': 'k', 'BP': 'p',
        'WR': 'R', 'WN': 'N', 'WB': 'B', 'WQ': 'Q', 'WK': 'K', 'WP': 'P'
        }
        if self.white:
            turn = 'w'
        else:
            turn = "b"

        castling = ''
        if self.white:
            if isinstance(self.board[7][4], King) and not self.board[7][4].moved:
                if isinstance(self.board[7][7], Rook) and not self.board[7][7].moved:
                    castling += 'K'
                if isinstance(self.board[7][0], Rook) and not self.board[7][0].moved:
                    castling += 'Q'
            if isinstance(self.board[0][4], King) and not self.board[0][4].moved:
                if isinstance(self.board[0][7], Rook) and not self.board[0][7].moved:
                    castling += 'k'
                if isinstance(self.board[0][0], Rook) and not self.board[0][0].moved:
                    castling += 'q'
        else:
            if isinstance(self.board[0][3], King) and not self.board[0][3].moved:
                if isinstance(self.board[0][0], Rook) and not self.board[0][0].moved:
                    castling += 'K'
                if isinstance(self.board[0][7], Rook) and not self.board[0][7].moved:
                    castling += 'Q'
            if isinstance(self.board[7][3], King) and not self.board[7][3].moved:
                if isinstance(self.board[7][0], Rook) and not self.board[7][0].moved:
                    castling += 'k'
                if isinstance(self.board[7][7], Rook) and not self.board[7][7].moved:
                    castling += 'q'
        if castling == '':
            castling = '-'
        
        board = self.formattedBoard()
        if not self.white:
            board = self.reversedBoard(board)
        rowsFEN = []

        for row in board:
            emptyCount = 0
            rowFEN = ""
            
            for square in row:
                if square == 0:
                    emptyCount += 1
                else:
                    if emptyCount > 0:
                        rowFEN += str(emptyCount)
                        emptyCount = 0
                    rowFEN += pieceMap[square]
                    
            if emptyCount > 0:
                rowFEN += str(emptyCount)
                
            rowsFEN.append(rowFEN)
            
        # Join the rows with slashes
        layout = "/".join(rowsFEN)
        
        # FEN requires 6 parts separated by spaces
        return f"{layout} {turn} {castling} {enPassant} {self.halfMoves} {self.fullMoves}"

    def uciToGameFormat(self, uci):
        """Convert a UCI string to the program's coordinate system."""
        startX = ord(uci[0]) - ord('a')
        endX = ord(uci[2]) - ord('a')
        startY = 8 - int(uci[1])
        endY = 8 - int(uci[3])
        
        promotion = uci[4] if len(uci) > 4 else None
        if promotion == 'q':
            promotion = Queen()
        elif promotion == 'r':
            promotion = Rook()
        elif promotion == 'b':
            promotion = Bishop()
        elif promotion == 'n':
            promotion = Knight()
        
        return (startX, startY), (endX, endY), promotion

    def getStockfishMove(self, fen):
        """Pass the FEN to the wrapper and extract both best and ponder moves."""
        self.stockfish.set_fen_position(fen)
        bestMove = self.stockfish.get_best_move()
        raw = self.stockfish.raw_stockfish_output(self.stockfish.get_best_move)
        ponder = None
        eval = self.stockfish.get_evaluation()

        for line in raw:
            if line.startswith("bestmove"):
                parts = line.split()
                # Line format: bestmove e2e4 ponder g8f6
                if len(parts) >= 4 and parts[2] == "ponder":
                    ponder = parts[3]
                break
        return bestMove, ponder, eval

    def run(self):
        """Run turns, update the board, and enforce game-ending conditions."""
        self.runs = True
        moves = []
        if self.timer and not self.playStockfish:
            self.turnStarted = monotonic()

        while self.runs:
            toSkip = False

            if self.timer and not self.playStockfish:
                self.gui.refresh(self.formattedBoard(), self.formatTime(), self.dotBoard)
            else:
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
            # Repetition is counted against the saved positions in the game history.
            for state in self.moves:
                if state == self.board:
                    repetition += 1
            if repetition == 3:
                self.draw(2) # Repetition
            if self.halfMoves >= 100:
                self.draw(4) # 50-move rule
            if self.timer and not self.playStockfish and self.remainingTime[self.white] - self.elapsedTime <= 0:
                if len(otherIF) <= 2 and otherPieces == otherIF:
                    self.draw(1) # On time by insufficient material
                else:
                    self.win(1) # On time

            if not self.runs:
                while True:
                    inp = self.gui.waitClick()
                    if inp is None or inp == '_S':
                        return

            if not self.playStockfish:
                if self.timer:
                    inp = self.gui.waitClick(monotonic())
                else:
                    inp = self.gui.waitClick()
            else:
                if self.white == self.playingWhite:
                    inp = self.gui.waitClick()
            # print(inp)

            if inp == '_L':
                self.previousMoves()

            if inp == "_T":
                continue

            if inp == '_S':
                return

            if inp.upper() == 'F':
                try:
                    print(self.getStockfishMove(self.formatFEN()))
                except:
                    pass

            if inp.upper() == 'A':
                try:
                    print(self.formatFEN())
                except:
                    pass

            if moves != []:
                for move in moves:
                    if isinstance(move[0],tuple): # en passant logic
                        if move[0] == inp and isinstance(self.board[piece[1]][piece[0]], Pawn):
                            self.board[inp[1]][inp[0]] = self.board[piece[1]][piece[0]]
                            self.board[piece[1]][piece[0]] = 0
                            self.board[move[1][1]][move[1][0]] = 0
                            self.halfMoves = 0
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
                            self.halfMoves += 1
                            self.reverse()
                            self.moves.append([row.copy() for row in self.board])
                            toSkip = True
                            # print(self.isInCheck())
                            break
                    if move == inp:
                        self.board[inp[1]][inp[0]] = self.board[piece[1]][piece[0]]
                        self.board[piece[1]][piece[0]] = 0
                        if inp[1] == 0 and isinstance(self.board[inp[1]][inp[0]], Pawn):
                            # Automatically promote to a queen unless manual choice is enabled.
                            if self.autoPromote:
                                self.board[inp[1]][inp[0]] = Queen(self.white)
                            else:
                                self.board[inp[1]][inp[0]] = self.manualPromotion()
                                if isinstance(self.board[inp[1]][inp[0]], Rook):
                                    self.board[inp[1]][inp[0]].moved = True
                        elif isinstance(self.board[inp[1]][inp[0]], King):
                            self.board[inp[1]][inp[0]].moved = True
                        elif isinstance(self.board[inp[1]][inp[0]], Rook):
                            self.board[inp[1]][inp[0]].moved = True
                        if self.moves[-1][inp[1]][inp[0]] != 0 or isinstance(self.board[inp[1]][inp[0]], Pawn):
                            self.halfMoves = 0
                        else:
                            self.halfMoves += 1
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

class Knight:
    """Represent a knight and calculate its legal destination candidates."""

    def __init__(self, White: bool):
        """Create a knight with the given side color."""
        self.white = White

    def clicked(self, inp, Game, check: bool = False):
        """Return available knight moves and the piece's current coordinates."""
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

class Bishop:
    """Represent a bishop and calculate its legal destination candidates."""

    def __init__(self, White: bool):
        """Create a bishop with the given side color."""
        self.white = White

    def clicked(self, inp, Game, check: bool = False):
        """Return available bishop moves and the piece's current coordinates."""
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

class Rook:
    """Represent a rook and calculate its legal destination candidates."""

    def __init__(self, White: bool):
        """Create a rook and mark it as unmoved."""
        self.white = White
        self.moved = False

    def clicked(self, inp, Game, check: bool = False):
        """Return available rook moves and the piece's current coordinates."""
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

class King:
    """Represent a king and calculate its legal destination candidates."""

    def __init__(self, White: bool):
        """Create a king and mark it as unmoved."""
        self.white = White
        self.moved = False

    def clicked(self, inp, Game, check: bool = False):
        """Return available king moves and the piece's current coordinates."""
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
                # A rook must be present and unmoved, with clear squares between it and the king.
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

class Queen:
    """Represent a queen and calculate its legal destination candidates."""

    def __init__(self, White: bool):
        """Create a queen with the given side color."""
        self.white = White

    def clicked(self, inp, Game, check: bool = False):
        """Return available queen moves and the piece's current coordinates."""
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

class Pawn:
    """Represent a pawn and calculate its legal destination candidates."""

    def __init__(self, White: bool):
        """Create a pawn with the given side color."""
        self.white = White

    def clicked(self, inp, Game, check: bool = False):
        """Return available pawn moves and the piece's current coordinates."""
        moves = []
        if check:
            # Pawns attack diagonally even when the target square is empty.
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
                
        if Game.white == self.white:
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
                if inp[0] < 7 and len(Game.moves) >= 2:
                    piece = Game.board[inp[1]][inp[0]+1]
                    if isinstance(Game.moves[-2][inp[1]-2][inp[0]+1], Pawn) and Game.moves[-1][inp[1]-2][inp[0]+1] == 0 and isinstance(Game.moves[-1][inp[1]][inp[0]+1], Pawn):
                        moves.append(((inp[0]+1,inp[1]-1),(inp[0]+1,inp[1])))   
        return moves, inp

# -------------------------------- Main program ------------------------------- #

if __name__ == "__main__":
    game = Game()

# Boards for tests:
# game = Game([[Rook(False), Knight(False), Bishop(False), King(False), Queen(False), Bishop(False), Knight(False), Rook(False)]] + [[Pawn(False) for i in range(8)]] + [[0 for i in range(8)]] + [[0,0,0,0,0,0,0,0]] + [[0 for i in range(8)] for j in range(2)] + [[Pawn(True) for i in range(8)]] + [[Rook(True), Knight(True), Bishop(True), King(True), Queen(True), Bishop(True), Knight(True), Rook(True)]])
# game = Game([[0, 0, 0, King(False), 0, 0, 0, 0]] + [[0 for i in range(8)] for j in range(6)] + [[0, 0, 0, King(True), Queen(True), 0, 0, 0]])