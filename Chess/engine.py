import numpy as np


class State:
    """This class represents the state of the chess game."""

    def __init__(self):
        """Initialize the chess board and pieces."""
        self.board = np.array(
            [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ]
        )
        self.white_to_move = True  # first move is white
        self.move_log = []  # list of moves made

    def makeMove(self, move) -> None:
        """Make a move on the board."""
        self.board[move.startRow][move.startCol] = "."  # inital square has to be empty
        self.board[move.endRow][
            move.endCol
        ] = move.pieceMoved  # move the piece to the new square
        self.move_log.append(move)  # for history of moves
        self.white_to_move = not self.white_to_move  # swapping players

    def undoMove(self) -> None:
        """Undo the last move."""
        if len(self.move_log) != 0:
            move = self.move_log.pop()  # get the last move
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.white_to_move = not self.white_to_move
        else:
            print("No moves to undo.")

    # going for move selection and validation
    def getValidMoves(self) -> list:
        """Get all valid moves for the current player."""
        valid_moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != "." and (
                    piece[0] == "w" if self.white_to_move else piece[0] == "b"
                ):
                    valid_moves.extend(self.getPieceMoves(r, c))
        return valid_moves

    # selecting a piece and getting its valid moves
    def getPieceMoves(self, r, c) -> list:
        """Get all valid moves for a piece."""
        piece = self.board[r][c]
        if piece[1] == "p":
            return self.getPawnMoves(r, c)
        elif piece[1] == "R":
            return self.getRookMoves(r, c)
        elif piece[1] == "N":
            return self.getKnightMoves(r, c)
        elif piece[1] == "B":
            return self.getBishopMoves(r, c)
        elif piece[1] == "Q":
            return self.getQueenMoves(r, c)
        elif piece[1] == "K":
            return self.getKingMoves(r, c)
        return []

    def getPawnMoves(self, r, c) -> list:
        """Get all valid moves for a pawn."""

        # just for reference of coding purposes bro.
        """
        FOR CODING PURPOSES I WILL BE USING THIS NOTATION:
                  col 0 col 1 col 2 col 3 col 4 col 5 col 6 col 7
            row 0 Rook Knight Bishop Queen King Bishop Knight Rook
            row 1  <--------------Black pawns----------------->
            row 2
            row 3
            row 4
            row 5
            row 6  <--------------White pawns----------------->
            row 7 Rook Knight Bishop Queen King Bishop Knight Rook
        
        """
        moves = []
        direction = (
            -1 if self.white_to_move else 1
        )  # white pawn will move up the board, hence -1, # black pawn will move down the board, hence 1
        start_row = (
            6 if self.white_to_move else 1
        )  # starting row for white pawn is 6, black pawn is 1
        if self.board[r + direction][c] == ".":
            moves.append(((r, c), (r + direction, c)))  # can move one square forward
        if r == start_row and self.board[r + 2 * direction][c] == ".":
            moves.append(
                ((r, c), (r + 2 * direction, c))
            )  # can move two squares from starting position
        if c - 1 >= 0 and self.board[r + direction][c - 1] != ".":
            moves.append(((r, c), (r + direction, c - 1)))  # left diagonal capture
        if c + 1 < 8 and self.board[r + direction][c + 1] != ".":
            moves.append(((r, c), (r + direction, c + 1)))  # right diagonal capture
        return moves

    def getRookMoves(self, r, c) -> list:
        """Get all valid moves for a rook."""
        moves = []
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]  # vertical and horizontal -> (row, col)
        for direction in directions:
            for i in range(1, 8):
                new_r = r + direction[0] * i
                new_c = c + direction[1] * i
                if 0 <= new_r < 8 and 0 <= new_c < 8:
                    if self.board[new_r][new_c] == ".":
                        moves.append(((r, c), (new_r, new_c)))  # empty square
                    elif self.board[new_r][new_c][0] != self.board[r][c][0]:
                        moves.append(
                            ((r, c), (new_r, new_c))
                        )  # if it is an enemy piece, capture it
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c) -> list:
        """Get all valid moves for a knight."""
        moves = []
        knight_moves = [
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ]
        for move in knight_moves:
            new_r = r + move[0]
            new_c = c + move[1]
            if 0 <= new_r < 8 and 0 <= new_c < 8:
                if self.board[new_r][new_c] == ".":
                    moves.append(((r, c), (new_r, new_c)))
                elif self.board[new_r][new_c][0] != self.board[r][c][0]:
                    moves.append(((r, c), (new_r, new_c)))
        return moves

    def getBishopMoves(self, r, c) -> list:
        """Get all valid moves for a bishop."""
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for direction in directions:
            for i in range(1, 8):
                new_r = r + direction[0] * i  # we can move ith square in the direction
                new_c = c + direction[1] * i
                if 0 <= new_r < 8 and 0 <= new_c < 8:
                    if self.board[new_r][new_c] == ".":
                        moves.append(((r, c), (new_r, new_c)))
                    elif self.board[new_r][new_c][0] != self.board[r][c][0]:
                        moves.append(((r, c), (new_r, new_c)))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c) -> list:
        """Get all valid moves for a queen."""
        moves = []
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        for direction in directions:
            for i in range(1, 8):
                new_r = r + direction[0] * i
                new_c = c + direction[1] * i
                if 0 <= new_r < 8 and 0 <= new_c < 8:
                    if self.board[new_r][new_c] == ".":
                        moves.append(((r, c), (new_r, new_c)))
                    elif self.board[new_r][new_c][0] != self.board[r][c][0]:
                        moves.append(((r, c), (new_r, new_c)))
                        break
                    else:
                        break
                else:
                    break

    def getKingMoves(self, r, c) -> list:
        """Get all valid moves for a king."""
        moves = []
        king_moves = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]
        for move in king_moves:
            new_r = r + move[0]
            new_c = c + move[1]
            if 0 <= new_r < 8 and 0 <= new_c < 8:
                if self.board[new_r][new_c] == ".":
                    moves.append(((r, c), (new_r, new_c)))
                elif self.board[new_r][new_c][0] != self.board[r][c][0]:
                    moves.append(((r, c), (new_r, new_c)))
        return moves


class Move:
    """This class represents a move in chess."""

    # just a dictionary to convert between ranks and rows, files and columns
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    # s, e => tuple: start square location, end square location
    def __init__(self, s, e, board):
        self.startRow = s[0]
        self.startCol = s[1]
        self.endRow = e[0]
        self.endCol = e[1]
        self.pieceMoved = board[s[0]][s[1]]
        self.pieceCaptured = board[e[0]][e[1]]

    # just for debugging purposes
    def getChessNotation(self) -> str:
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(
            self.endRow, self.endCol
        )

    def getRankFile(self, r, c) -> str:
        # convert the row and column to rank and file
        return self.colsToFiles[c] + self.rowsToRanks[r]
