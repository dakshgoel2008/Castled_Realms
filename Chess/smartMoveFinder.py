import random

from config import CHECKMATE, DEPTH, PIECE_SQUARE_TABLES, PIECESCORE, STALEMATE


class TranspositionTable:
    """Simple transposition table for memoization"""

    def __init__(self):
        self.table = {}

    def get(self, board_hash, depth):
        key = (board_hash, depth)
        return self.table.get(key)

    def store(self, board_hash, depth, score, move):
        key = (board_hash, depth)
        self.table[key] = (score, move)

    def clear(self):
        self.table.clear()


transposition_table = TranspositionTable()


def findRandomMove(validMoves):
    """Select a random move from the list of valid moves."""
    return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)  # Shuffle to add randomness in AI's choice
    counter = 0  # Reset the counter for move evaluations
    findNegaMaxMoveWithAlphaBeta(
        gs,
        validMoves,
        DEPTH,
        1 if gs.white_to_move else -1,
        -float("inf"),
        float("inf"),
    )
    print(f"Evaluated {counter} positions")
    return nextMove


def orderMoves(gs, moves):
    """Order moves for better alpha-beta pruning"""

    def moveValue(move):
        # Prioritize captures
        if gs.board[move.endRow][move.endCol] != ".":
            captured_piece = gs.board[move.endRow][move.endCol][1]
            moving_piece = move.pieceMoved[1]
            # MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
            return PIECESCORE[captured_piece] - PIECESCORE[moving_piece]

        # Prioritize center control
        center_bonus = 0
        if move.endRow in [3, 4] and move.endCol in [3, 4]:
            center_bonus = 10

        return center_bonus

    return sorted(moves, key=moveValue, reverse=True)


def findNegaMaxMoveWithAlphaBeta(gs, validMoves, depth, turnMultiplier, alpha, beta):
    """Enhanced NegaMax with alpha-beta pruning and optimizations"""
    global nextMove, counter
    counter += 1

    # Check transposition table
    board_hash = hash(str(gs.board))
    tt_entry = transposition_table.get(board_hash, depth)
    if tt_entry and depth < DEPTH:  # Don't use TT for root
        return tt_entry[0]

    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # Order moves for better pruning
    validMoves = orderMoves(gs, validMoves)

    maxScore = -float("inf")
    bestMove = None

    for move in validMoves:
        gs.makeMove(move)
        score = -findNegaMaxMoveWithAlphaBeta(
            gs, gs.getValidMoves(), depth - 1, -turnMultiplier, -beta, -alpha
        )
        gs.undoMove()

        if score > maxScore:
            maxScore = score
            bestMove = move
            if depth == DEPTH:
                nextMove = move

        # Alpha-beta pruning
        alpha = max(alpha, maxScore)
        if alpha >= beta:
            break  # Beta cutoff

    # Store in transposition table
    if bestMove:
        transposition_table.store(board_hash, depth, maxScore, bestMove)

    return maxScore


def scoreBoard(gs):
    """Enhanced board evaluation with positional factors"""
    if gs.checkMate == "checkmate":
        return -CHECKMATE if gs.white_to_move else CHECKMATE
    elif gs.checkMate == "stalemate":
        return STALEMATE

    score = 0

    for row in range(8):
        for col in range(8):
            piece = gs.board[row][col]
            if piece == ".":
                continue

            color = piece[0]
            piece_type = piece[1]

            # Material value
            piece_value = PIECESCORE[piece_type]

            # Positional value from piece-square tables
            if color == "w":
                positional_value = PIECE_SQUARE_TABLES[piece_type][row][col]
                score += piece_value + positional_value
            else:
                # Flip the table for black pieces
                positional_value = PIECE_SQUARE_TABLES[piece_type][7 - row][col]
                score -= piece_value + positional_value

    # Additional positional factors
    score += evaluateKingSafety(gs)
    score += evaluatePawnStructure(gs)
    score += evaluateMobility(gs)

    return score


# TODO: will improve this
def evaluateKingSafety(gs):
    """Evaluate king safety"""
    # will imprpove it a bit later.
    safety_score = 0

    # Find kings
    white_king_pos = None   
    black_king_pos = None

    for row in range(8):
        for col in range(8):
            piece = gs.board[row][col]
            if piece == "wK":
                white_king_pos = (row, col)
            elif piece == "bK":
                black_king_pos = (row, col)

    # Penalize exposed kings (simplified)
    if white_king_pos:
        row, col = white_king_pos
        if row > 1:  # King moved from back rank
            safety_score -= 30

    if black_king_pos:
        row, col = black_king_pos
        if row < 6:  # King moved from back rank
            safety_score += 30

    return safety_score


def evaluatePawnStructure(gs):
    """Evaluate pawn structure"""
    pawn_score = 0
    white_pawns = []
    black_pawns = []

    # Collect pawn positions
    for row in range(8):
        for col in range(8):
            piece = gs.board[row][col]
            if piece == "wp":
                white_pawns.append((row, col))
            elif piece == "bp":
                black_pawns.append((row, col))

    # Check for doubled pawns
    white_files = [col for row, col in white_pawns]
    black_files = [col for row, col in black_pawns]

    for file in range(8):
        white_count = white_files.count(file)
        black_count = black_files.count(file)

        if white_count > 1:
            pawn_score -= 10 * (white_count - 1)
        if black_count > 1:
            pawn_score += 10 * (black_count - 1)

    return pawn_score


# currently it is only woking for Knight but haver to implement other pieces functionality also.
def evaluateMobility(gs):
    """Evaluate piece mobility"""
    mobility_score = 0

    # Knights in center are more mobile and also covers more squares.
    for row in range(8):
        for col in range(8):
            piece = gs.board[row][col]
            # piece is a knight
            if piece in ["wN", "bN"]:
                center_distance = abs(row - 3.5) + abs(col - 3.5)
                mobility_bonus = max(0, 7 - center_distance) * 2

                if piece == "wN":
                    mobility_score += mobility_bonus
                else:
                    mobility_score -= mobility_bonus

            # if piece is a bishop
            # if piece in ["wB", "bB"]:


            # piece is a rook
            # if piece in ["wR", "bR"]:

            # piece is a Queen
            # if piece in ["wQ", "bQ"]:

    return mobility_score
