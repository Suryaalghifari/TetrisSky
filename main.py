import pygame
import random
import os
from game_logic import Tetrimino, check_collision, clear_lines, shapes, colors
from game_view import draw_grid, draw_ghost, draw_score

def start_screen(screen, font):
    running = True
    button_color = (0, 200, 0)
    button_hover_color = (0, 255, 0)
    button_rect = pygame.Rect(100, 250, 100, 50)
    while running:
        screen.fill((0, 0, 0)) 
        title_text = font.render("Genjor Tetris", True, (255, 255, 255))
        screen.blit(title_text, (75, 150))

        # event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False 

  
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            color = button_hover_color
        else:
            color = button_color

      
        pygame.draw.rect(screen, color, button_rect)
        button_text = font.render("Start", True, (0, 0, 0))
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))

        pygame.display.flip()

# Logic Tampilan Game Over
def game_over_screen(screen, font, score):
    running = True
    button_color= (200, 0, 0)
    button_hover_color = (255, 0, 0)
    button_rect = pygame.Rect(100, 250, 100, 50)
    
    while running:
        screen.fill((0, 0, 0))
        game_over_text = font.render("GAME OVER", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(game_over_text, (75, 150))
        screen.blit(score_text, (100, 200))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return
                
        mouse_pos = pygame.mouse.get_pos()
        color = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color
        
        pygame.draw.rect(screen, color, button_rect)
        button_text = font.render("Restart", True, (0, 0 , 0))
        screen.blit(button_text, (button_rect.x + 10, button_rect.y +10))

        pygame.display.flip()
        




def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 600))
    font = pygame.font.Font(None, 36)

   
    start_screen(screen, font)

    # Variabel permainan
    clock = pygame.time.Clock()
    block_size = 30
    columns, rows = 10, 20
    grid = [[0 for _ in range(columns)] for _ in range(rows)]

    current_tetrimino = Tetrimino(columns // 2 - 1, 0, random.choice(shapes))
    next_tetrimino = Tetrimino(columns // 2 - 1, 0, random.choice(shapes))

    fall_time = 0
    fall_speed = 0.1
    running = True
    score = 0
    lines_cleared = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Logika Mouse
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                new_x = mouse_x // block_size
                if new_x != current_tetrimino.x:
                    current_tetrimino.x = new_x
                    if check_collision(grid, current_tetrimino.shape, (current_tetrimino.x, current_tetrimino.y)):
                        current_tetrimino.x = max(0, min(current_tetrimino.x, columns - len(current_tetrimino.shape[0])))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Klik kiri
                    while not check_collision(grid, current_tetrimino.shape, (current_tetrimino.x, current_tetrimino.y + 1)):
                        current_tetrimino.y += 1
                    print("Tetromino dropped!")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetrimino.x -= 1
                    if check_collision(grid, current_tetrimino.shape, (current_tetrimino.x, current_tetrimino.y)):
                        current_tetrimino.x += 1

                if event.key == pygame.K_RIGHT:
                    current_tetrimino.x += 1
                    if check_collision(grid, current_tetrimino.shape, (current_tetrimino.x, current_tetrimino.y)):
                        current_tetrimino.x -= 1

                if event.key == pygame.K_DOWN:
                    current_tetrimino.y += 1
                    if check_collision(grid, current_tetrimino.shape, (current_tetrimino.x, current_tetrimino.y)):
                        current_tetrimino.y -= 1

                if event.key == pygame.K_UP:
                    current_tetrimino.rotate()
                    if check_collision(grid, current_tetrimino.shape, (current_tetrimino.x, current_tetrimino.y)):
                        for _ in range(3):
                            current_tetrimino.rotate()

        fall_time += clock.get_time() / 1000
        clock.tick(60)

        if fall_time >= fall_speed:
            fall_time = 0
            current_tetrimino.y += 1
            if check_collision(grid, current_tetrimino.shape, (current_tetrimino.x, current_tetrimino.y)):
                current_tetrimino.y -= 1
                for y, row in enumerate(current_tetrimino.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            grid[current_tetrimino.y + y][current_tetrimino.x + x] = current_tetrimino.color
                current_tetrimino = next_tetrimino
                next_tetrimino = Tetrimino(columns // 2 - 1, 0, random.choice(shapes))
                lines = clear_lines(grid)
                if lines > 0:
                    lines_cleared += lines 
                    base_score = 100
                    bonus = (lines - 1) * 50
                    score += lines * base_score + bonus
                
                # Manggil Tampilan Awal After Game Over
                if any(grid[0]):
                    game_over_screen(screen, font, score)
                    return

        # Rendering
        screen.fill(colors[0])
        draw_grid(screen, grid, colors, block_size)
        draw_ghost(screen, grid, current_tetrimino, block_size)
        draw_score(screen, font, score, lines_cleared)

        for y, row in enumerate(current_tetrimino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        colors[current_tetrimino.color],
                        ((current_tetrimino.x + x) * block_size, (current_tetrimino.y + y) * block_size, block_size, block_size)
                    )

        pygame.display.flip()

    print(f"Game Over! Your Score: {score}")
    pygame.quit()

if __name__ == "__main__":
    while True:
        main()
