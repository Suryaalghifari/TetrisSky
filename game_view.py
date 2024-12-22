import pygame
from game_logic import check_collision


def draw_grid(screen, grid, colors, block_size):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    colors[cell],
                    (x * block_size, y * block_size, block_size, block_size)
                )


def draw_ghost(screen, grid, tetrimino, block_size):
    ghost_y = tetrimino.y
    while not check_collision(grid, tetrimino.shape, (tetrimino.x, ghost_y)):
        ghost_y += 1
    ghost_y -= 1
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    (200, 200, 200),
                    ((tetrimino.x + x) * block_size, (ghost_y + y) * block_size, block_size, block_size),
                    1
                )

def draw_score(screen, font, score, lines_cleared):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {lines_cleared // 5}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))
