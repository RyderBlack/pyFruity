import pygame
import glob, random
from sys import exit
import time

# Init pygame and screen
WIDTH, HEIGHT = 800,450
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT ))
pygame.display.set_caption('Intro Pygame')
clock = pygame.time.Clock()

# Create font
my_main_font = pygame.font.Font('fonts/Pixeltype.ttf', 80)
timer_font = pygame.font.Font('fonts/Pixeltype.ttf', 50)
letter_font = pygame.font.Font('fonts/Pixeltype.ttf', 50)

# Environment
slicer_bg_surface = pygame.image.load('graphics/environments/slicer_bg.png').convert()

# Game name
game_name_surface = my_main_font.render('Pixel Fruit Slicer', False, (211,166,139))
game_name_rect = game_name_surface.get_rect(center=(400,80))

