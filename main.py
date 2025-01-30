"""
slice 1 fruit >> point +1
slice multiple fruits == combo
if fruits missed or not sliced == 1 strike
if 3 strike == game over
slice bomb == game over
if slice ice cube> time frozen 3-5sec
final score == nb fruits sliced in 1 game
create menu
"""

import pygame
import glob, random
from sys import exit

WIDTH, HEIGHT = 800,450

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT ))
pygame.display.set_caption('Intro Pygame')
# to control FPS
clock = pygame.time.Clock()

#random fruit picked
file_path = ["./graphics/fruits/*.png"]
images = glob.glob(random.choice(file_path))
random_image = random.choice(images)


# create Text and font
my_main_font = pygame.font.Font('fonts/Pixeltype.ttf', 80)

# environment
slicer_bg_surface = pygame.image.load('graphics/environments/slicer_bg.png').convert()

# game name
game_name_surface = my_main_font.render('Pixel Fruit Slicer', False, (211,166,139))
game_name_rect = game_name_surface.get_rect(center=(400,80))

# fruit 
fruit_surface = pygame.image.load(random_image).convert_alpha()
# fruit_surface = pygame.transform.rotozoom(fruit_surface, 0, 2)
fruit_surface = pygame.transform.scale2x(fruit_surface)
fruit_rect = fruit_surface.get_rect(center=(200,300))

# Fruit Physics
fruit_x = random.randint(50, WIDTH - 50)  # Random start x-position
fruit_y = HEIGHT                           # Start at the bottom
fruit_x_velocity = random.choice([-3, -2, -1, 1, 2, 3])  # Random horizontal velocity
fruit_y_velocity = -15                     # Launch velocity (upward)
gravity = 0.5                              # Pulls the fruit downward

# Game Variables
strikes = 0        # Missed fruits
game_over = False  # Game Over flag

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # Background
    screen.blit(slicer_bg_surface, (0, 0))
    screen.blit(game_name_surface, game_name_rect)
    
    # Update Fruit Position
    fruit_y_velocity += gravity  # Gravity reduces y_velocity over time
    fruit_x += fruit_x_velocity  # Update horizontal position
    fruit_y += fruit_y_velocity  # Update vertical position
    
    # Respawn Fruit if it Falls Off-Screen
    if fruit_y > HEIGHT:
        strikes += 1  # Increment strikes if fruit falls
        fruit_x = random.randint(50, WIDTH - 50)  # Reset horizontal position
        fruit_y = HEIGHT  # Reset to bottom
        fruit_y_velocity = -15  # Reset launch velocity
        fruit_x_velocity = random.choice([-3, -2, -1, 1, 2, 3])  # Random x velocity
    
    # Game Over Condition
    if strikes == 3:
        game_over = True
        break

    # Draw Fruit
    fruit_rect.center = (fruit_x, fruit_y)  # Update fruit rect position
    screen.blit(fruit_surface, fruit_rect)
    
    # Update Display
    pygame.display.update()
    clock.tick(60)