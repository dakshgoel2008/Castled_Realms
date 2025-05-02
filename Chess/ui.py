import os
import pygame as p
from config import SQUARE_SIZE, DIMENSION, WIDTH, HEIGHT, MAX_FPS


def load_images() -> dict[str, p.Surface]:
    """Load and return scaled chess piece images."""
    pieces = ['wB', 'wK', 'wN', 'wp', 'wQ', 'wR', 'bB', 'bK', 'bN', 'bp', 'bQ', 'bR']
    images = {}
    for piece in pieces:
        path = os.path.join('Chess', 'images', f'{piece}.png')
        images[piece] = p.transform.scale(p.image.load(path), (SQUARE_SIZE, SQUARE_SIZE))
    return images

def draw_game_state(screen: p.Surface, board: list[list[str]], images: dict[str, p.Surface],
                    selected_sq: tuple, valid_moves: list[tuple]) -> None:
    draw_board(screen)
    draw_labels(screen, p.font.SysFont('Arial', 18))
    highlight_squares(screen, selected_sq, valid_moves)
    draw_pieces(screen, board, images)


def draw_board(screen: p.Surface) -> None:
    
    """Draw the chess board squares."""
    colors = [p.Color(255, 206, 158), p.Color(209, 139, 71)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen: p.Surface, board: list[list[str]], images: dict[str, p.Surface]) -> None:

    """Draw the pieces on top of the board."""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '.':
                rect = p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                screen.blit(images[piece], rect)

# Highlight squares
def highlight_squares(screen, selected_sq, valid_moves):
    if selected_sq:
        r, c = selected_sq
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('blue'))
        screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))

        s.fill(p.Color('yellow'))
        for move in valid_moves:
            start, end = move
            if start == selected_sq:
                er, ec = end
                screen.blit(s, (ec * SQUARE_SIZE, er * SQUARE_SIZE))


# Draw coordinate labels
def draw_labels(screen, font):
    for i in range(DIMENSION):
        # Files (a-h)
        label = font.render(chr(ord('a') + i), True, p.Color('black'))
        screen.blit(label, (i * SQUARE_SIZE + SQUARE_SIZE//2 - label.get_width()//2, HEIGHT - label.get_height()))
        # Ranks (1-8)
        label = font.render(str(DIMENSION - i), True, p.Color('black'))
        screen.blit(label, (0, i * SQUARE_SIZE + SQUARE_SIZE//2 - label.get_height()//2))
