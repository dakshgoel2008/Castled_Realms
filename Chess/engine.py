import numpy as np

"""
    My Chess Board:
    0  bR  bN  bB  bQ  bK  bB  bN  bR
    1  bp  bp  bp  bp  bp  bp  bp  bp
    2  .   .   .   .   .   .   .   .
    3  .   .   .   .   .   .   .   .
    4  .   .   .   .   .   .   .   .
    5  .   .   .   .   .   .   .   .
    6  wp  wp  wp  wp  wp  wp  wp  wp
    7  wR  wN  wB  wQ  wK  wB  wN  wR
    -  a   b   c   d   e   f   g   h
"""


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
        self.white_to_move = True  # first move is white (According to chess rules)
        self.move_log = []  # list of moves made
        self.whiteKingLoc = (7, 4)  #
        self.blackKingLoc = (0, 4)
        # En passant target square - stores the square behind the pawn that just moved two squares
        self.enpassant_possible = ()  # (row, col) of the square where en passant capture is possible
        # Castling rights:
        self.currentCastlingRights = CastleRights(
            True, True, True, True
        )  # initially castling is true
        self.castleRightsLog = [
            CastleRights(
                self.currentCastlingRights.whiteKingSide,
                self.currentCastlingRights.whiteQueenSide,
                self.currentCastlingRights.blackKingSide,
                self.currentCastlingRights.blackQueenSide,
            )
        ]

    def makeMove(self, move) -> None:
        """Make a move on the board."""
        self.board[move.startRow][move.startCol] = "."  # initial square has to be empty
        # move the piece to the new square
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.move_log.append(move)  # for history of moves
        self.white_to_move = not self.white_to_move  # swapping players

        # if king is moved take the record of the new positions of the king
        if move.pieceMoved == "wK":
            self.whiteKingLoc = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLoc = (move.endRow, move.endCol)

        # pawn promotion:
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + "Q"

        # En passant move handling
        if move.isEnpassantMove:
            # Remove the captured pawn (which is not on the end square)
            self.board[move.startRow][move.endCol] = "."  # Remove the captured pawn

        # Update en passant possibility

        # only the pawn which have the right to move two squares can be set as the en passant target square

        # for my understanding:
        """        . . P2 . .      . . . . .     . . . . .
                   . . . . .   ->  . . . . .  -> . . P1 . .
                   . P1 . . .      . P1 P2 .     . . . . .
        """
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.enpassant_possible = (
                (move.startRow + move.endRow) // 2,
                move.startCol,  # col remains the same
            )
        else:
            self.enpassant_possible = ()

        # castle moves:
        if move.isCastleMove:
            # king side castle:
            if move.endCol - move.startCol == 2:
                # copies rook to new position
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][
                    move.endCol + 1
                ]
                # remove it from previous position
                self.board[move.endRow][move.endCol + 1] = "."
            # Queen side castle:
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][
                    move.endCol - 2
                ]
                self.board[move.endRow][move.endCol - 2] = "."
        # updating the castling rights - If the king or rook has moved for once the castling rights will be vanished away.
        self.updateCastleRights(move)
        self.castleRightsLog.append(
            CastleRights(
                self.currentCastlingRights.whiteKingSide,
                self.currentCastlingRights.whiteQueenSide,
                self.currentCastlingRights.blackKingSide,
                self.currentCastlingRights.blackQueenSide,
            )
        )
        #

    def undoMove(self) -> None:
        """Undo the last move."""
        # atleast move_log has to have something for deletion.
        if len(self.move_log) != 0:
            move = self.move_log.pop()  # get the last move
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][
                move.endCol
            ] = (
                move.pieceCaptured
            )  # initially pieceCaptured was empty bro so don't think of that case.
            self.white_to_move = (
                not self.white_to_move
            )  # now change the player dude to undo other player's move.

            # Restore king position: Badshah ko alag se sahi rakhna padega bro. Nahi to destruction🔥
            if move.pieceMoved == "wK":
                self.whiteKingLoc = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLoc = (move.startRow, move.startCol)

            # handling en passant undo
            if move.isEnpassantMove:
                # Restore the captured pawn
                captured_pawn = "bp" if move.pieceMoved[0] == "w" else "wp"
                self.board[move.startRow][
                    move.endCol
                ] = captured_pawn  # can use any col both will be same.
                # Fix: The captured pawn should be placed at the correct location
                self.board[move.endRow][move.endCol] = "."

            # Restore en passant possibility from previous move
            if len(self.move_log) > 0:
                prev_move = self.move_log[-1]  # check from back bro.
                if (
                    prev_move.pieceMoved[1] == "p"
                    and abs(prev_move.startRow - prev_move.endRow) == 2
                ):
                    self.enpassant_possible = (
                        (prev_move.startRow + prev_move.endRow) // 2,
                        prev_move.startCol,
                    )
                else:
                    self.enpassant_possible = ()
            else:
                self.enpassant_possible = ()

            # undo the castling rights:
            self.castleRightsLog.pop()  # pop the recent rights to undo
            # set currentCastleRights = last one.
            if len(self.castleRightsLog) > 0:
                self.currentCastlingRights = self.castleRightsLog[-1]
            else:
                self.currentCastlingRights = CastleRights(True, True, True, True)

            # undo castle moves:
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # king side castle
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][
                        move.endCol - 1
                    ]
                    self.board[move.endRow][move.endCol - 1] = "."
                else:  # Queen side castle
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][
                        move.endCol + 1
                    ]
                    self.board[move.endRow][move.endCol + 1] = "."
            
            #TODO: logic for undoing check.
            

    # update castle rights:
    def updateCastleRights(self, move):
        """Updating the castling rights in given moves"""
        # if pieceMoved is a king. No possibility of castling in any circumstances.
        if move.pieceMoved == "wK":
            self.currentCastlingRights.whiteKingSide = False
            self.currentCastlingRights.whiteQueenSide = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRights.blackKingSide = False
            self.currentCastlingRights.blackQueenSide = False

        # if rook is 'the' pieceMoved.
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRights.whiteQueenSide = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRights.whiteKingSide = False

        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:  # left rook
                    self.currentCastlingRights.blackQueenSide = False
                elif move.startCol == 7:  # right rook
                    self.currentCastlingRights.blackKingSide = False

        # Also update castling rights when a rook is captured
        if move.pieceCaptured == "wR":
            if move.endRow == 7:
                if move.endCol == 0:  # left rook captured
                    self.currentCastlingRights.whiteQueenSide = False
                elif move.endCol == 7:  # right rook captured
                    self.currentCastlingRights.whiteKingSide = False
        elif move.pieceCaptured == "bR":
            if move.endRow == 0:
                if move.endCol == 0:  # left rook captured
                    self.currentCastlingRights.blackQueenSide = False
                elif move.endCol == 7:  # right rook captured
                    self.currentCastlingRights.blackKingSide = False

    # All pseudo moves of the pieces
    def getAllPseudoLegalMoves(self) -> list:
        # here we are just exploring all the moves possible.
        # Later will be optimising for valid moves only.
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != "." and (
                    piece[0] == "w" if self.white_to_move else piece[0] == "b"
                ):
                    piece_moves = self.getPieceMoves(r, c)
                    for start, end in piece_moves:
                        moves.append(Move(start, end, self.board))

        return moves

    # going for move selection and validation
    def getValidMoves(self) -> list:
        """Get all valid Move objects for the current player."""
        tempCastlingRights = CastleRights(
            self.currentCastlingRights.whiteKingSide,
            self.currentCastlingRights.whiteQueenSide,
            self.currentCastlingRights.blackKingSide,
            self.currentCastlingRights.blackQueenSide,
        )
        # getting first all the pseudo moves.
        moves = self.getAllPseudoLegalMoves()

        # just done here to avoid infinite recursion
        if self.white_to_move:
            self.getCastleMoves(self.whiteKingLoc[0], self.whiteKingLoc[1], moves)
        else:
            self.getCastleMoves(self.blackKingLoc[0], self.blackKingLoc[1], moves)
        # the trick is to move backwards through the moves and check if the king is in check after making each move -> moving backwards helps to avoid cases when we iterate through the list and remove elements from it and can't access the next element as it is shifted to the left
        for i in range(len(moves) - 1, -1, -1):

            # NERD approach
            # TODO: Will modify this approach for better performance
            self.makeMove(moves[i])
            self.white_to_move = (
                not self.white_to_move
            )  # generate all the moves for the opponent first and check the positions where opponents can attack the king of current player

            if self.inCheck():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move

            # now undo the move to restore the board state
            self.undoMove()
        self.currentCastlingRights = tempCastlingRights
        return moves

    def inCheck(self) -> bool:
        # check for those squares which can be attacked to conquer the king of particular side
        if self.white_to_move:
            return self.squareUnderAttack(
                self.whiteKingLoc[0], self.whiteKingLoc[1]
            )  # (r, c)
        else:
            return self.squareUnderAttack(self.blackKingLoc[0], self.blackKingLoc[1])

    def squareUnderAttack(self, r, c) -> bool:
        # this is very obvious code bro.

        self.white_to_move = not self.white_to_move  # toggle the players
        opponent_moves = self.getAllPseudoLegalMoves()
        self.white_to_move = not self.white_to_move

        for move in opponent_moves:
            if move.endRow == r and move.endCol == c:
                return True

        return False

    def checkMate(self) -> str:
        if not self.getValidMoves():  # if no valid moves available
            if (
                self.inCheck()
            ):  # either it will be a checkmate or stalemate if still there's a check
                return "checkmate"
            else:
                return "stalemate"
        elif (
            self.inCheck()
        ):  # if valid moves available and in check ask the player to shut mind off and move his required move
            return "check"
        else:
            return "play"  # already in good position bro, just play your game.

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
        moves = []
        direction = (
            -1 if self.white_to_move else 1
        )  # white pawn will move up the board, hence -1, # black pawn will move down the board, hence 1
        start_row = (
            6 if self.white_to_move else 1
        )  # starting row for white pawn is 6, black pawn is 1

        # Forward moves
        if 0 <= r + direction < 8 and self.board[r + direction][c] == ".":
            moves.append(((r, c), (r + direction, c)))  # can move one square forward
            # Two square move from starting position
            if r == start_row and self.board[r + 2 * direction][c] == ".":
                moves.append(
                    ((r, c), (r + 2 * direction, c))
                )  # can move two squares from starting position but only once

        # Diagonal captures
        for dc in [-1, 1]:  # Check both diagonal directions
            if 0 <= c + dc < 8 and 0 <= r + direction < 8:
                target = self.board[r + direction][c + dc]
                if target != "." and target[0] != self.board[r][c][0]:
                    moves.append(((r, c), (r + direction, c + dc)))

        # En passant capture
        if len(self.enpassant_possible) != 0:
            # Fix: En passant logic - the capturing pawn moves to the en passant square
            if (
                r == (3 if self.white_to_move else 4)
                and abs(c - self.enpassant_possible[1]) == 1
                and r + direction == self.enpassant_possible[0]
            ):
                moves.append(
                    (
                        (r, c),
                        (self.enpassant_possible[0], self.enpassant_possible[1]),
                    )
                )

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

    # generating all valid castling moves:
    def getCastleMoves(self, r, c, moves) -> None:
        if self.squareUnderAttack(r, c):
            return  # castling not allowed if in check

        if (self.white_to_move and self.currentCastlingRights.whiteKingSide) or (
            not self.white_to_move and self.currentCastlingRights.blackKingSide
        ):
            self.getKingSideCastleMoves(r, c, moves)

        if (self.white_to_move and self.currentCastlingRights.whiteQueenSide) or (
            not self.white_to_move and self.currentCastlingRights.blackQueenSide
        ):
            self.getQueenSideCastleMoves(r, c, moves)

    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == "." and self.board[r][c + 2] == ".":
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(
                r, c + 2
            ):
                # Fix: Create Move object properly
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if (
            self.board[r][c - 1] == "."
            and self.board[r][c - 2] == "."
            and self.board[r][c - 3] == "."
        ):
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(
                r, c - 2
            ):
                # Fix: Create Move object properly
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))


# castling rights:
class CastleRights:
    def __init__(self, whiteKingSide, whiteQueenSide, blackKingSide, blackQueenSide):
        self.whiteKingSide = whiteKingSide
        self.whiteQueenSide = whiteQueenSide
        self.blackKingSide = blackKingSide
        self.blackQueenSide = blackQueenSide


class Move:
    """This class represents a move in chess."""

    # just a dictionary to convert between ranks and rows, files and columns
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {
        v: k for k, v in ranksToRows.items()
    }  # just reversing the ranks and rows
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {
        v: k for k, v in filesToCols.items()
    }  # just reversing the files and columns

    def __init__(self, startSq, endSq, board, isCastleMove=False):
        self.startRow = startSq[0]  # initial position of a piece (startRow, startCol)
        self.startCol = startSq[1]
        self.endRow = endSq[0]  # final position of a piece (endRow, endCol)
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # pawn promotion:
        self.isPawnPromotion = False
        if (self.pieceMoved == "wp" and self.endRow == 0) or (
            self.pieceMoved == "bp" and self.endRow == 7
        ):
            self.isPawnPromotion = True

        # En passant detection
        self.isEnpassantMove = False
        if self.pieceMoved[1] == "p":
            if (self.endCol != self.startCol) and self.pieceCaptured == ".":
                self.isEnpassantMove = True

        # castle Move:
        self.isCastleMove = isCastleMove

        # Unique ID for the move
        self.moveID = (
            self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        )

    def __eq__(self, other):  # just for comparing the moves
        if isinstance(other, Move):
            return (
                self.moveID == other.moveID
            )  # use of moveId helped a lot for unique identification -> using technique learned in Rabin Karp algorithm (ashing)
        return False

    def __hash__(self):  # just allow me to use the moves in a set
        return hash(self.moveID)

    # just for debugging purposes
    def getChessNotation(self) -> str:
        # Add 'e.p.' suffix for en passant moves
        notation = self.getRankFile(self.startRow, self.startCol) + self.getRankFile(
            self.endRow, self.endCol
        )
        if self.isEnpassantMove:
            notation += " e.p."
        return notation

    def getRankFile(self, r, c) -> str:
        # convert the row and column to rank and file
        return self.colsToFiles[c] + self.rowsToRanks[r]
