import pygame
import random

# pygame module for loading and rendering fonts
pygame.font.init()

# 10x20 grid
screen_width = 700
screen_height = 1000
play_width = 300 # 30 width per block for 10 blocks
play_height = 600 # 30 height per block for 20 blocks
block_size = 30

# top-left xy coordinates (origin frame of reference)
top_left_x = (screen_width - play_width) // 2
top_left_y = (screen_height - play_height) // 2

# tetrominoes schematic
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
pieces = [S, Z, I, O, J, L, T]
piece_colors = [(5, 196, 107), (255, 82, 82), (0, 216, 214), (255, 165, 2), (56, 103, 214), (255, 121, 63), (136, 84, 208)]