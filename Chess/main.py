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
                loc = p.mouse.get_pos()  # to get the mouse position
                col = loc[0] // (
                    SQUARE_SIZE
                )  # on dividing the x coordinate by the square size we will get the column
                row = loc[1] // (SQUARE_SIZE)  # same for row also

                if row >= DIMENSION or col >= DIMENSION:
                    continue

                if sqSelected == (row, col):  # if the user clicks the same square again
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                """If it was a 2nd click, make a move"""
                # TODO: Have to work on those scenerios where user clicks on wrong position the game is getting closed

                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:  # if the move is valid
                            gs.makeMove(validMoves[i])  # thus make the required move
                            moveMade = True
                        sqSelected = ()  # reset the square selected and player clicks
                        playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]

            # Keys pressed handler.
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # for better user experience
                    gs.undoMove()
                    moveMade = True
                # Not allowing the redo 😇 -> for obvious reasons.

        if moveMade:
            validMoves = (
                gs.getValidMoves()
            )  # again find the valid moves at some instance
            moveMade = False
        draw_game_state(screen, gs.board, images, sqSelected, validMoves, gs)
        draw_labels(screen, font)
        clock.tick(MAX_FPS)  # TODO: update this later.
        p.display.flip()  # pygame display update


if __name__ == "__main__":
    main()
