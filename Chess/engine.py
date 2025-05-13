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
        """Get all valid Move objects for the current player."""
        valid_moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != "." and (
                    piece[0] == "w" if self.white_to_move else piece[0] == "b"
                ):
                    piece_moves = self.getPieceMoves(r, c)
                    for start, end in piece_moves:
                        valid_moves.append(
                            Move(start, end, self.board)
                        )  # wrap in Move class
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

    # just for reference of coding purposes bro.
    """
        <=======================NOTATION=====================>:
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

    def getPawnMoves(self, r, c) -> list:
        """Get all valid moves for a pawn."""
        moves = []
        direction = (
            -1 if self.white_to_move else 1
        )  # white pawn will move up the board, hence -1, # black pawn will move down the board, hence 1
        start_row = (
            6 if self.white_to_move else 1
        )  # starting row for white pawn is 6, black pawn is 1
        if self.board[r + direction][c] == ".":
            moves.append(((r, c), (r + direction, c)))  # can move one square forward
        if (
            r == start_row
            and self.board[r + direction][c] == "."
            and self.board[r + 2 * direction][c] == "."
        ):
            moves.append(
                ((r, c), (r + 2 * direction, c))
            )  # can move two squares from starting position but only once
        if c - 1 >= 0:
            target = self.board[r + direction][c - 1]
            if target != "." and target[0] != self.board[r][c][0]:
                moves.append(((r, c), (r + direction, c - 1)))
        if c + 1 < 8:
            target = self.board[r + direction][c + 1]
            if target != "." and target[0] != self.board[r][c][0]:
                moves.append(((r, c), (r + direction, c + 1)))

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
        return moves

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
        return moves

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
        return moves

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
    rowsToRanks = {
        v: k for k, v in ranksToRows.items()
    }  # just reversing the ranks and rows
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # Unique ID for the move
        self.moveID = (
            self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        )

    def __eq__(self, other):  # just for comparing the moves
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def __hash__(self):  # just allow me to use the moves in a set
        return hash(self.moveID)

    # just for debugging purposes
    def getChessNotation(self) -> str:
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(
            self.endRow, self.endCol
        )

    def getRankFile(self, r, c) -> str:
        # convert the row and column to rank and file
        return self.colsToFiles[c] + self.rowsToRanks[r]
