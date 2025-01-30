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
import time

# init pygame and screen
WIDTH, HEIGHT = 800,450
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT ))
pygame.display.set_caption('Intro Pygame')

# create Text and font
my_main_font = pygame.font.Font('fonts/Pixeltype.ttf', 80)
timer_font = pygame.font.Font('fonts/Pixeltype.ttf', 50)

# Time related variables
clock = pygame.time.Clock()
game_duration = 60
start_time = time.time()
remaining_time = game_duration

# timer surface
timer_surface = timer_font.render(f'Time: {remaining_time}', False, (211,166,139))
timer_rect = timer_surface.get_rect(topright=(WIDTH-20, 20))

#random fruit image picked
file_path = ["./graphics/fruits/*.png"]
images = glob.glob(random.choice(file_path))
random_image = random.choice(images)

# environment
slicer_bg_surface = pygame.image.load('graphics/environments/slicer_bg.png').convert()

# game name
game_name_surface = my_main_font.render('Pixel Fruit Slicer', False, (211,166,139))
game_name_rect = game_name_surface.get_rect(center=(400,80))

# fruits surface
fruit_surface = pygame.image.load(random_image).convert_alpha()
# fruit_surface = pygame.transform.rotozoom(fruit_surface, 0, 2)
fruit_surface = pygame.transform.scale2x(fruit_surface)
fruit_rect = fruit_surface.get_rect(center=(200,300))

# Fruit Physics
fruit_x = random.randint(50, WIDTH - 50)
fruit_y = HEIGHT
fruit_x_velocity = random.choice([-3, -2, -1, 1, 2, 3])
fruit_y_velocity = -15
gravity = 0.5

# Game Variables
strikes = 0
game_over = False
MENU_STATE = "menu"

class Button:
    def __init__(self, x, y, width, height, text, font_size=50):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font('fonts/Pixeltype.ttf', font_size)
        self.color = (211,166,139)
        self.hover_color = (180,140,120)
        self.text_color = (255,255,255)

    def draw_button(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos): color = self.hover_color
        else: color = self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Buttons
play_button = Button(WIDTH//2 - 100, HEIGHT//2 - 50, 200, 50, "Play")
quit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "Quit")

def reset_game():
    global fruit_x, fruit_y, fruit_x_velocity, fruit_y_velocity, strikes, game_over, start_time
    fruit_x = random.randint(50, WIDTH - 50)
    fruit_y = HEIGHT
    fruit_x_velocity = random.choice([-3, -2, -1, 1, 2, 3])
    fruit_y_velocity = -15
    strikes = 0
    game_over = False
    start_time = time.time()

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        #menu
        if MENU_STATE == "menu":
            if play_button.handle_event(event):
                MENU_STATE = "game"
                reset_game()
            if quit_button.handle_event(event):
                pygame.quit()
                exit()
                
    # Background
    screen.blit(slicer_bg_surface, (0, 0))
    screen.blit(game_name_surface, game_name_rect)
    
    if MENU_STATE == "menu":
        # Affichage du menu
        play_button.draw_button(screen)
        quit_button.draw_button(screen)
    
    elif MENU_STATE == "game":
        # Timer
        remaining_time = max(game_duration - int(time.time() - start_time), 0)
        timer_surface = timer_font.render(f'Time: {remaining_time}', False, (211,166,139))
        screen.blit(timer_surface, timer_rect)
        
        if remaining_time == 0:
            MENU_STATE = "menu"
            continue
        

        # Display fruit
        fruit_y_velocity += gravity
        fruit_x += fruit_x_velocity
        fruit_y += fruit_y_velocity
        
        if fruit_y > HEIGHT:
            strikes += 1
            fruit_x = random.randint(50, WIDTH - 50)
            fruit_y = HEIGHT
            fruit_y_velocity = -15
            fruit_x_velocity = random.choice([-3, -2, -1, 1, 2, 3])
            
        if strikes == 3 and remaining_time == 0:
            MENU_STATE = "menu"
            continue

        # Draw Fruit
        fruit_rect.center = (fruit_x, fruit_y)
        screen.blit(fruit_surface, fruit_rect)
    
    # Update Display
    pygame.display.update()
    clock.tick(60)