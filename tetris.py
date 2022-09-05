import pygame
import random

# pygame module for loading and rendering fonts
pygame.font.init()

# 10x20 grid
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 1000
COLUMNS = 10
ROWS = 20
BLOCK_SIZE = 30
PLAY_WIDTH = 300 # 30 width per block for 10 blocks
PLAY_HEIGHT = 600 # 30 height per block for 20 blocks

# top-left xy coordinates (origin frame of reference)
top_left_x = (SCREEN_WIDTH - PLAY_WIDTH) // 2
top_left_y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 2

# tetromino schematic
S = [['....', 
      '.00.', 
      '00..', 
      '....'], 
     ['0...', 
      '00..', 
      '.0..', 
      '....']]

Z = [['....', 
      '.00.', 
      '..00', 
      '....'], 
     ['...0', 
      '..00', 
      '..0.', 
      '....']]

I = [['.0..', 
      '.0..', 
      '.0..', 
      '.0..'], 
     ['....', 
      '0000', 
      '....', 
      '....']]

O = [['....', 
      '.00.', 
      '.00.', 
      '....']]

J = [['0...', 
      '000.', 
      '....', 
      '....'],
     ['.00.', 
      '.0..', 
      '.0..', 
      '....'],
     ['....', 
      '000', 
      '..0.', 
      '....'],
     ['.0..', 
      '.0..', 
      '00..', 
      '....']]

L = [['...0', 
      '.000', 
      '....', 
      '....'],
     ['..0.', 
      '..0.', 
      '..00', 
      '....'],
     ['....', 
      '.000', 
      '.0..', 
      '....'],
     ['.00.', 
      '..0.', 
      '..0.', 
      '....']]

T = [['.0..', 
      '000.', 
      '....', 
      '....'],
     ['.0..', 
      '.00.', 
      '.0..', 
      '....'],
     ['....', 
      '000.', 
      '.0..', 
      '....'],
     ['.0..', 
      '00..', 
      '.0..', 
      '....']]

# Green S, Red Z, Cyan I, Yellow O, Blue J, Orange L, Purple T
piece_types = [S, Z, I, O, J, L, T]
piece_colors = [(5, 196, 107), (255, 82, 82), (0, 216, 214), (255, 165, 2), (56, 103, 214), (255, 121, 63), (136, 84, 208)]

class Piece(object):
    def __init__(self, column, row, piece):
        self.x = column
        self.y = row
        self.piece = piece
        self.color = piece_colors[piece_types.index(piece)]
        self.rotation = 0

def create_grid(locked_positions = {}):
    grid = [[(0,0,0) for _ in range(COLUMNS)] for _ in range(ROWS)]
    # rows: y-axis, columns: x-axis
    for y in range(ROWS):
        for x in range(COLUMNS):
            if (x, y) in locked_positions:
                block_color = locked_positions[(x, y)]
                grid[y][x] = block_color
    return grid

def draw_grid(surface, grid):
    for y in range(ROWS):
        for x in range(COLUMNS):
            block_x = (top_left_x + (x * BLOCK_SIZE))
            block_y = (top_left_y + (y * BLOCK_SIZE))
            pygame.draw.rect(surface, grid[y][x], (block_x, block_y), BLOCK_SIZE, BLOCK_SIZE, 0)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y), PLAY_WIDTH, PLAY_HEIGHT, 4)

def draw_window(surface, grid):
    surface.fill((0, 0, 0))
    font = pygame.font.SysFont()
    title = font.render('Tetris', 1, (255, 255, 255))
    title_x = top_left_x + (PLAY_WIDTH / 2) - (title.get_width() / 2)
    title_y = top_left_y + (PLAY_HEIGHT / 2) - (title.get_height() / 2)
    surface.blit(title, (title_x, title_y))

    draw_grid(surface, grid)
    pygame.display.update()

def get_random_shape():
    return random.choice(piece_types)







    