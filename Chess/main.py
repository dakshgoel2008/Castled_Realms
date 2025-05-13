import pygame as p
from config import DIMENSION, HEIGHT, MAX_FPS, SQUARE_SIZE, WIDTH
from engine import Move, State
from ui import draw_game_state, draw_labels, load_images


def main() -> None:
    """Main game loop."""
    p.init()
    p.display.set_caption("Chess")
    screen = p.display.set_mode((WIDTH, HEIGHT))  # size of the window
    clock = p.time.Clock()
    gs = State()
    images = load_images()
    validMoves = gs.getValidMoves()  # finding all the valid moves at current state
    moveMade = False  # initially no move made
    sqSelected = ()  # will be defined once user makes a click
    playerClicks = []  # keep track of player clicks (two tuples)
    # playerOne = True  # True if human, False if AI
    font = p.font.SysFont("Times New Roman", 18)
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos()
                col = loc[0] // (SQUARE_SIZE)
                row = loc[1] // (SQUARE_SIZE)
                if sqSelected == (row, col):  # if the user clicks the same square again
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                """If it was a 2nd click, make a move"""
                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    if move in validMoves:  # if the move is valid
                        gs.makeMove(move)  # thus make the required move
                        moveMade = True
                    sqSelected = ()  # reset the square selected and player clicks
                    playerClicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # for better user experience
                    gs.undoMove()
                    moveMade = True
                # Not allowing the redo 😇

        if moveMade:
            validMoves = (
                gs.getValidMoves()
            )  # again find the valid moves at some instance
            moveMade = False
        draw_game_state(screen, gs.board, images, sqSelected, validMoves)
        draw_labels(screen, font)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
