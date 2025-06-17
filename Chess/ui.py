import math
import os

import pygame as p
from config import ANIMATION_DURATION, DIMENSION, HEIGHT, SQUARE_SIZE, WIDTH


def load_images() -> dict[str, p.Surface]:
    """Load and return scaled chess piece images."""
    pieces = ["wB", "wK", "wN", "wp", "wQ", "wR", "bB", "bK", "bN", "bp", "bQ", "bR"]
    images = {}
    for piece in pieces:
        path = os.path.join("Chess", "images", f"{piece}.png")
        images[piece] = p.transform.scale(
            p.image.load(path), (SQUARE_SIZE, SQUARE_SIZE)
        )
    return images


def draw_game_state(
    screen,
    board,
    images,
    selected_sq,
    valid_moves,
    gs,
    animating_move=None,
    animation_progress=0,
) -> None:
    draw_board(screen)
    draw_labels(screen, p.font.SysFont("Arial", 18))
    highlight_squares(screen, selected_sq, valid_moves, gs)

    # Draw pieces with animation
    if animating_move:
        draw_pieces_with_animation(
            screen, board, images, animating_move, animation_progress
        )
    else:
        draw_pieces(screen, board, images)


def animate_move(screen, board, images, move, gs, clock):
    """Animate a chess move from start to end position."""
    start_time = p.time.get_ticks()

    # Calculate start and end positions in pixels
    start_x = move.startCol * SQUARE_SIZE
    start_y = move.startRow * SQUARE_SIZE
    end_x = move.endCol * SQUARE_SIZE
    end_y = move.endRow * SQUARE_SIZE

    # Store the piece being moved
    piece = move.pieceMoved

    # Temporarily remove piece from board for animation
    temp_board = board.copy()
    temp_board[move.startRow][move.startCol] = "."

    while True:
        current_time = p.time.get_ticks()
        elapsed = current_time - start_time

        if elapsed >= ANIMATION_DURATION:
            break

        # Calculate animation progress (0 to 1)
        progress = elapsed / ANIMATION_DURATION
        # Use easing function for smoother animation
        progress = ease_in_out(progress)

        # Calculate current position
        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress

        # Draw everything
        draw_board(screen)
        draw_labels(screen, p.font.SysFont("Arial", 18))

        # Draw all pieces except the moving one
        draw_pieces(screen, temp_board, images)

        # Draw the moving piece at current position
        screen.blit(images[piece], (current_x, current_y))

        # Handle special moves during animation
        if move.isCastleMove:
            animate_castling_rook(screen, images, move, progress)

        p.display.flip()
        clock.tick(60)  # 60 FPS for smooth animation


def animate_castling_rook(screen, images, move, progress):
    """Animate the rook movement during castling."""
    if move.endCol - move.startCol == 2:  # King side castle
        rook_start_col = 7
        rook_end_col = 5
    else:  # Queen side castle
        rook_start_col = 0
        rook_end_col = 3

    rook_piece = "wR" if move.pieceMoved == "wK" else "bR"

    # Calculate rook positions
    rook_start_x = rook_start_col * SQUARE_SIZE
    rook_end_x = rook_end_col * SQUARE_SIZE
    rook_y = move.startRow * SQUARE_SIZE

    # Current rook position
    current_rook_x = rook_start_x + (rook_end_x - rook_start_x) * progress

    screen.blit(images[rook_piece], (current_rook_x, rook_y))


def ease_in_out(t):
    """Easing function for smoother animation."""
    return t * t * (3.0 - 2.0 * t)


def draw_board(screen) -> None:
    """Draw the chess board squares."""
    colors = [p.Color(255, 206, 158), p.Color(209, 139, 71)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) & 1]
            p.draw.rect(
                screen,
                color,
                p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )


def draw_pieces(screen, board, images) -> None:
    """Draw the pieces on top of the board."""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != ".":
                rect = p.Rect(
                    c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                )
                screen.blit(images[piece], rect)


def draw_pieces_with_animation(screen, board, images, animating_move, progress):
    """Draw pieces with one piece being animated."""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "." and not (
                r == animating_move.startRow and c == animating_move.startCol
            ):
                rect = p.Rect(
                    c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                )
                screen.blit(images[piece], rect)

    # Draw the animating piece
    start_x = animating_move.startCol * SQUARE_SIZE
    start_y = animating_move.startRow * SQUARE_SIZE
    end_x = animating_move.endCol * SQUARE_SIZE
    end_y = animating_move.endRow * SQUARE_SIZE

    current_x = start_x + (end_x - start_x) * progress
    current_y = start_y + (end_y - start_y) * progress

    screen.blit(images[animating_move.pieceMoved], (current_x, current_y))


def highlight_squares(screen, selected_sq, valid_moves, gs) -> None:
    """Highlight selected square, valid moves, and game state indicators."""
    if selected_sq:
        r, c = selected_sq
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color("blue"))
        screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))

        s.fill(p.Color("yellow"))
        for move in valid_moves:
            if move.startRow == r and move.startCol == c:
                er = move.endRow
                ec = move.endCol
                screen.blit(s, (ec * SQUARE_SIZE, er * SQUARE_SIZE))

    if gs.inCheck():
        king_row, king_col = gs.whiteKingLoc if gs.white_to_move else gs.blackKingLoc
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color("red"))
        screen.blit(s, (king_col * SQUARE_SIZE, king_row * SQUARE_SIZE))

    if gs.checkMate() == "checkmate":
        s = p.Surface((WIDTH, HEIGHT))
        s.set_alpha(100)
        s.fill(p.Color("green"))
        screen.blit(s, (0, 0))
        text = p.font.SysFont("Times New Roman", 40).render(
            "Checkmate! " + ("White" if not gs.white_to_move else "Black") + " wins",
            True,
            p.Color("black"),
        )
        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2),
        )

    if gs.checkMate() == "stalemate":
        s = p.Surface((WIDTH, HEIGHT))
        s.set_alpha(100)
        s.fill(p.Color("green"))
        screen.blit(s, (0, 0))
        text = p.font.SysFont("Times New Roman", 50).render(
            "Stalemate!", True, p.Color("black")
        )
        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2),
        )


def draw_labels(screen, font) -> None:
    """Draw coordinate labels."""
    for i in range(DIMENSION):
        # Files (a-h)
        label = font.render(chr(ord("a") + i), True, p.Color("black"))
        screen.blit(
            label,
            (
                i * SQUARE_SIZE + SQUARE_SIZE // 2 - label.get_width() // 2,
                HEIGHT - label.get_height(),
            ),
        )
        # Ranks (1-8)
        label = font.render(str(DIMENSION - i), True, p.Color("black"))
        screen.blit(
            label, (0, i * SQUARE_SIZE + SQUARE_SIZE // 2 - label.get_height() // 2)
        )


# Additional animation utilities
def animate_capture(screen, images, captured_piece, position, clock):
    """Animate piece capture with fade out effect."""
    start_time = p.time.get_ticks()
    fade_duration = 200

    while True:
        current_time = p.time.get_ticks()
        elapsed = current_time - start_time

        if elapsed >= fade_duration:
            break

        progress = elapsed / fade_duration
        alpha = int(255 * (1 - progress))

        # Create fading piece surface
        piece_surface = images[captured_piece].copy()
        piece_surface.set_alpha(alpha)

        screen.blit(piece_surface, position)
        p.display.flip()
        clock.tick(60)


def animate_check_warning(screen, king_pos, clock):
    """Animate a pulsing red highlight for check warning."""
    start_time = p.time.get_ticks()
    pulse_duration = 500

    while True:
        current_time = p.time.get_ticks()
        elapsed = current_time - start_time

        if elapsed >= pulse_duration:
            break

        progress = elapsed / pulse_duration
        # Create pulsing effect
        alpha = int(100 + 100 * math.sin(progress * math.pi * 4))

        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(alpha)
        s.fill(p.Color("red"))
        screen.blit(s, (king_pos[1] * SQUARE_SIZE, king_pos[0] * SQUARE_SIZE))

        p.display.flip()
        clock.tick(60)
