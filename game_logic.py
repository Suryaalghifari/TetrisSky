import random

# Konstanta
colors = [
    (0, 0, 0), 
    (255, 0, 0),  
    (0, 255, 0),  
    (0, 0, 255),  
    (255, 255, 0),  
    (255, 165, 0), 
    (128, 0, 128), 
    (0, 255, 255)  
]

shapes = [
    [[1, 1, 1, 1]],  # Garis
    [[1, 1], [1, 1]],  # Kotak
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# Kelas 
class Tetrimino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.randint(1, len(colors) - 1)

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


def check_collision(grid, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = off_x + x
                new_y = off_y + y
                if new_x < 0 or new_x >= len(grid[0]) or new_y >= len(grid):
                    return True
                if new_y >= 0 and grid[new_y][new_x]:  # Periksa tabrakan dengan grid
                    return True
    return False


def clear_lines(grid):
    full_rows = [i for i, row in enumerate(grid) if all(row)]
    for i in full_rows:
        del grid[i]
        grid.insert(0, [0] * len(grid[0]))
    return len(full_rows)
