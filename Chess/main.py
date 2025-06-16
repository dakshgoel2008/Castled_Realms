import pygame as p
from config import DIMENSION, HEIGHT, MAX_FPS, SQUARE_SIZE, WIDTH
from engine import Move, State
from ui import animate_move, draw_game_state, draw_labels, load_images


def main() -> None:
    """Main game loop."""
    p.init()
    p.display.set_caption("Chess")
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = State()
    images = load_images()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False

    sqSelected = ()
    playerClicks = []
    font = p.font.SysFont("Times New Roman", 18)
    running = True

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                loc = p.mouse.get_pos()
                col = loc[0] // SQUARE_SIZE
                row = loc[1] // SQUARE_SIZE

                if row >= DIMENSION or col >= DIMENSION:
                    continue

                # If no square selected yet or clicked same color piece again
                if not sqSelected or (
                    gs.board[row][col] != "."
                    and gs.board[row][col][0]
                    == gs.board[sqSelected[0]][sqSelected[1]][0]
                ):
                    sqSelected = (row, col)
                    playerClicks = [sqSelected]
                else:
                    # Second click - attempt to make a move
                    move = Move(playerClicks[0], (row, col), gs.board)
                    for validMove in validMoves:
                        if move == validMove:
                            animate = True
                            animate_move(screen, gs.board, images, move, gs, clock)
                            gs.makeMove(validMove)
                            moveMade = True
                            animate = False
                            sqSelected = ()
                            playerClicks = []
                            break
                    else:
                        # Invalid move - select new piece if clicked on own piece
                        if gs.board[row][col] != "." and gs.board[row][col][0] == (
                            "w" if gs.white_to_move else "b"
                        ):
                            sqSelected = (row, col)
                            playerClicks = [sqSelected]
                        else:
                            sqSelected = ()
                            playerClicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    sqSelected = ()
                    playerClicks = []

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        draw_game_state(screen, gs.board, images, sqSelected, validMoves, gs)
        draw_labels(screen, font)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
