import numpy as np

class State():
    '''This class represents the state of the chess game.'''

    def __init__(self):
        '''Initialize the chess board and pieces.'''
        self.board = np.array([
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ])
        self.white_to_move = True   # first move is white
        self.move_log = []          # list of moves made

    def makeMove(self, move):
        '''Make a move on the board.'''
        self.board[move.startRow][move.startCol] = "." # inital square has to be empty
        self.board[move.endRow][move.endCol] = move.pieceMoved # move the piece to the new square
        self.move_log.append(move)  # for history of moves
        self.white_to_move = not self.white_to_move # swapping players
        
class Move():
    '''This class represents a move in chess.'''
    
    # just a dictionary to convert between ranks and rows, files and columns
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
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
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        # convert the row and column to rank and file
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
