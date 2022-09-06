from signal import SIG_DFL
import pygame
import random

# initialize all pygame modules (font, display, etc.)
pygame.init()

# 10x20 grid
SCREEN_WIDTH = 950
SCREEN_HEIGHT = 950
COLUMNS = 10
ROWS = 20
BLOCK_SIZE = 40
PLAY_WIDTH = 400 # 30 width per block for 10 blocks
PLAY_HEIGHT = 800 # 30 height per block for 20 blocks
WINDOW_COLOR = (10, 15, 20)
PLAY_COLOR = (20, 30, 40)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# top-left xy coordinates (origin frame of reference)
top_left_x = ((SCREEN_WIDTH / 2) - PLAY_WIDTH)
top_left_y = (SCREEN_HEIGHT - PLAY_HEIGHT) // 1.5

# tetromino schematic
S = [['.00.', 
      '00..',
      '....', 
      '....'], 
     ['0...', 
      '00..', 
      '.0..', 
      '....']]

Z = [['00..', 
      '.00.',
      '....', 
      '....'], 
     ['..0.', 
      '.00.', 
      '.0..', 
      '....']]

I = [['.0..', 
      '.0..', 
      '.0..', 
      '.0..'], 
     ['....', 
      '0000', 
      '....', 
      '....'],
     ['..0.', 
      '..0.', 
      '..0.', 
      '..0.'], 
     ['....',
      '....', 
      '0000',  
      '....']]

O = [['00..',
      '00..',
      '....', 
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

L = [['..0.', 
      '000.', 
      '....', 
      '....'],
     ['.0..', 
      '.0..', 
      '.00.', 
      '....'],
     ['....', 
      '000.', 
      '0...', 
      '....'],
     ['00..', 
      '.0..', 
      '.0..', 
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
    def __init__(self, column, row, piece_type):
        self.x = column
        self.y = row
        self.piece_type = piece_type
        self.color = piece_colors[piece_types.index(piece_type)]
        self.rotation = 0 # mod len(piece_type)

def create_grid(locked_positions):
    grid = [[PLAY_COLOR for _ in range(COLUMNS)] for _ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLUMNS):
            if (y, x) in locked_positions:
                block_color = locked_positions[(y, x)]
                grid[y][x] = block_color
    return grid

def draw_grid(surface):
    for y in range(ROWS):
        horizontal_start = (top_left_x, top_left_y + (y * BLOCK_SIZE))
        horizontal_end = (top_left_x + PLAY_WIDTH, top_left_y + (y * BLOCK_SIZE))
        pygame.draw.line(surface, BLACK, horizontal_start, horizontal_end)
        for x in range(COLUMNS):
            vertical_start = (top_left_x + (x * BLOCK_SIZE), top_left_y)
            vertical_end = (top_left_x + (x * BLOCK_SIZE), top_left_y + PLAY_HEIGHT)
            pygame.draw.line(surface, BLACK, vertical_start, vertical_end)
            
def draw_window(surface, grid):
    surface.fill(WINDOW_COLOR)
    font = pygame.font.SysFont('phosphate', 100)
    title = font.render('TETRIS', 1, WHITE)
    title_x = (SCREEN_WIDTH * 0.75) - (title.get_width() / 2)
    title_y = top_left_y
    surface.blit(title, (title_x, title_y))

    for y in range(ROWS):
        for x in range(COLUMNS):
            block_x = (top_left_x + (x * BLOCK_SIZE))
            block_y = (top_left_y + (y * BLOCK_SIZE))
            pygame.draw.rect(surface, grid[y][x], (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE), 0)
    pygame.draw.rect(surface, WHITE, (top_left_x - 5, top_left_y - 5, PLAY_WIDTH + 11, PLAY_HEIGHT + 11), 5)
    draw_grid(surface)

def draw_next_tetromino(piece, surface):
    font = pygame.font.SysFont('futura', 24)
    label = font.render('Next Tetromino', 1, WHITE)
    label_x = (SCREEN_WIDTH * 0.75) - (label.get_width() / 2)
    label_y = (top_left_y + PLAY_HEIGHT) / 2
    piece_orientation = piece.piece_type[piece.rotation]

    for y in range(len(piece_orientation)):
        for x in range(len(piece_orientation[y])):
            if piece_orientation[y][x] == '0':
                next_piece_x = (SCREEN_WIDTH * 0.75) - (BLOCK_SIZE * 1.5) + (x * BLOCK_SIZE)
                next_piece_y = label_y + (y * BLOCK_SIZE)
                pygame.draw.rect(surface, piece.color, (next_piece_x, next_piece_y, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(surface, BLACK, (next_piece_x, next_piece_y, BLOCK_SIZE, BLOCK_SIZE), 1)
    surface.blit(label, (label_x, label_y - (BLOCK_SIZE * 1.5)))

def get_random_piece():
    return Piece(5, 0, random.choice(piece_types))

def convert_piece_format(piece):
    positions = []
    orientation = piece.piece_type[piece.rotation]
    for delta_y in range(len(orientation)):
        for delta_x in range(len(orientation[delta_y])):
            if orientation[delta_y][delta_x] == '0':
                positions.append((piece.y + delta_y, piece.x + delta_x))
    return positions

def valid_location(piece, grid):
    accepted_locations = []
    for y in range(ROWS):
        for x in range(COLUMNS):
            if grid[y][x] == PLAY_COLOR:
                accepted_locations.append((y, x))

    formatted_piece_locations = convert_piece_format(piece)
    for position in formatted_piece_locations:
        if position not in accepted_locations:
            if position[0] > -1:
                return False
    return True

def check_failure(locked_positions):
    for position in locked_positions:
        if position[0] < 1:
            return True
    return False

def clear_rows(locked_positions, grid):
    shift = 0
    for y in range(ROWS - 1, -1, -1):
        # remove complete rows
        if PLAY_COLOR not in grid[y]:
            shift += 1
            for x in range(COLUMNS):
                if (y, x) in locked_positions:
                    del locked_positions[(y, x)]
        # shift other rows down            
        elif shift > 0:
            for x in range(COLUMNS):
                if (y, x) in locked_positions:
                    locked_positions[(y + shift, x)] = locked_positions.pop((y, x))

def main(surface):
    run = True
    locked_positions = {}
    current_piece = get_random_piece()
    next_piece = get_random_piece()
    change_piece = False

    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    fall_speed = 0.25

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # level up
        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.14:
                fall_speed -= 0.005

        # move piece down until collision
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_location(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # left-arrow key
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_location(current_piece, grid):
                        current_piece.x += 1
                # right-arrow key
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_location(current_piece, grid):
                        current_piece.x -= 1
                # down-arrow key
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_location(current_piece, grid):
                        current_piece.y -= 1
                # up-arrow key
                elif event.key == pygame.K_UP:
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.piece_type)
                    if not valid_location(current_piece, grid):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.piece_type)

        # display current piece in grid
        piece_locations = convert_piece_format(current_piece)
        for i in range(len(piece_locations)):
            y, x = piece_locations[i]
            if y > -1:
                grid[y][x] = current_piece.color
        
        # lock piece when it hits the ground
        if change_piece:
            for i in range(len(piece_locations)):
                locked_positions[piece_locations[i]] = current_piece.color
            current_piece = next_piece
            next_piece = get_random_piece()
            change_piece = False

            # clear rows if completed
            clear_rows(locked_positions, grid)
        
        # break loop when player loses
        if check_failure(locked_positions):
            run = False

        draw_window(surface, grid)
        draw_next_tetromino(next_piece, surface)
        pygame.display.update()
        
    pygame.display.quit()

def main_menu(window):
    main(window)

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
pygame.display.set_caption('Tetris')
main_menu(window)