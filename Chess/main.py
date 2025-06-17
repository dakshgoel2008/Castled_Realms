import pygame as p
from config import DIMENSION, HEIGHT, MAX_FPS, SQUARE_SIZE, WIDTH
from engine import Move, State
from smartMoveFinder import findRandomMove
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

    sqSelected = ()
    playerClicks = []
    font = p.font.SysFont("Times New Roman", 18)
    running = True
    # AI work
    playerOne = False  # True for humans and False for AI
    playerTwo = False  # initially AI move will be False
    gameOver = False

    while running:
        humanTurn = (gs.white_to_move and playerOne) or (
            not gs.white_to_move and playerTwo
        )
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
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
                                animate_move(screen, gs.board, images, move, gs, clock)
                                gs.makeMove(validMove)
                                moveMade = True
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
                if e.key == p.K_z and not gameOver:
                    gs.undoMove()
                    moveMade = True
                    sqSelected = ()
                    playerClicks = []
                    gameOver = False  # Reset game over state when undoing
                elif e.key == p.K_r and gameOver:
                    # Reset game when 'R' is pressed and game is over
                    gs = State()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    gameOver = False
                    moveMade = False

        # AI move finder:
        if not gameOver and not humanTurn:
            move = findRandomMove(validMoves)
            if move is not None:  # Check if AI found a valid move
                animate_move(screen, gs.board, images, move, gs, clock)
                gs.makeMove(move)
                moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

            # Check for game over conditions using your existing method
            game_status = gs.checkMate()
            if game_status == "checkmate" or game_status == "stalemate":
                gameOver = True

        draw_game_state(screen, gs.board, images, sqSelected, validMoves, gs)

        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
