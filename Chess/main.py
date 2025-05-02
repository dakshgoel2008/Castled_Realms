import pygame as p
from engine import State, Move
from ui import load_images, draw_game_state, highlight_squares, draw_labels
from config import SQUARE_SIZE, DIMENSION, WIDTH, HEIGHT, MAX_FPS


def main() -> None:
    """Main game loop."""
    p.init()
    p.display.set_caption('Chess')
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = State()
    images = load_images()
    sqSelected = ()
    playerClicks = []  # keep track of player clicks (two tuples)
    # playerOne = True  # True if human, False if AI
    
    font = p.font.SysFont('Times New Roman', 18)
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos()
                col = loc[0] // (SQUARE_SIZE)
                row = loc[1] // (SQUARE_SIZE)
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                
                '''If it what a 2nd click, make a move'''
                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []

                    
        draw_game_state(screen, gs.board, images, sqSelected, [])
        draw_labels(screen, font)
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()
