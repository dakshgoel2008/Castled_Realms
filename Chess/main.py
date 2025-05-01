import pygame as p
from engine import State

p.init()
p.font.init()
WIDTH = HEIGHT = 512  # 8x8 board
DIMENSION = 8  # chess board is 8x8
SQUARE_SIZE = HEIGHT // DIMENSION  # size of each square on the board
MAX_FPS = 15  # for animations
IMGS = {}

def load_images():
    '''Load images for the chess pieces.'''
    pieces = ['wB', 'wK', 'wN', 'wp', 'wQ', 'wR', 'bB', 'bK', 'bN', 'bp', 'bQ', 'bR']  # white and black pieces
    for piece in pieces:
        IMGS[piece] = p.transform.scale(p.image.load(f'Chess/images/{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE))
        IMGS[piece.upper()] = p.transform.scale(p.image.load(f'Chess/images/{piece.upper()}.png'), (SQUARE_SIZE, SQUARE_SIZE))

def main():
    '''Main function to run the chess game.'''
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    gs = State()  # initialize the game state
    load_images()  # load images for the pieces
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)  # control the frame rate
        p.display.flip()  # update the display

def draw_game_state(screen, gs):
    '''Draw the game state on the screen.'''
    draw_board(screen)  # draw the board
    # may be the suggestions also in future bro
    draw_pieces(screen, gs.board)  # draw the pieces on top of the board
    p.display.flip()  # update the display after drawing


def draw_board(screen):
    '''Draw the chess board.'''
    colors = [p.Color(255, 206, 158), p.Color(209, 139, 71)]  # light and dark squares
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]  # toggling colors for squares
            p.draw.rect(screen, color, p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # taking x * y coordinates of the square and drawing a rectangle on it

    
def draw_pieces(screen, board):
    '''Draw the pieces on the board.'''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]  # get the piece at the current square
            if piece != '.':
                screen.blit(IMGS[piece], p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # draw the piece



if __name__ == "__main__":
    # run the main function to start the game
    main()

