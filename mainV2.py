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
clock = pygame.time.Clock()

# create font
my_main_font = pygame.font.Font('fonts/Pixeltype.ttf', 80)
timer_font = pygame.font.Font('fonts/Pixeltype.ttf', 50)

# environment
slicer_bg_surface = pygame.image.load('graphics/environments/slicer_bg.png').convert()

# game name
game_name_surface = my_main_font.render('Pixel Fruit Slicer', False, (211,166,139))
game_name_rect = game_name_surface.get_rect(center=(400,80))

class Fruit:
    def __init__(self):
        self.file_path = "./graphics/fruits/*.png"
        self.images = glob.glob(self.file_path)
        # self.reset_fruit()
        
    def reset_fruit(self):
        # Position et physique
        self.x = random.randint(50, WIDTH - 50)
        self.y = HEIGHT
        self.x_velocity = random.choice([-3, -2, -1, 1, 2, 3])
        self.y_velocity = -15
        self.gravity = 0.5
        
        # Image
        random_image = random.choice(self.images)
        self.surface = pygame.image.load(random_image).convert_alpha()
        self.surface = pygame.transform.scale2x(self.surface)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        
    def update_fruit_physics(self):
        self.y_velocity += self.gravity
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.rect.center = (self.x, self.y)
        
        # check if fruit out of screen
        if self.y > HEIGHT:
            return True
        return False
        
    def draw_fruit(self, screen):
        screen.blit(self.surface, self.rect)

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


# Game Manager
class Game:
    def __init__(self):
        self.menu_state = "menu"
        self.strikes = 0
        self.game_over = False
        self.game_duration = 60
        self.start_time = time.time()
        self.remaining_time = self.game_duration
        self.fruit = Fruit()
        
        # Timer surface
        self.timer_surface = timer_font.render(f'Time: {self.remaining_time}', False, (211,166,139))
        self.timer_rect = self.timer_surface.get_rect(topright=(WIDTH-20, 20))
        
    def reset_game(self):
        self.strikes = 0
        self.game_over = False
        self.start_time = time.time()
        self.fruit.reset_fruit()
        
    def update_timer(self):
        self.remaining_time = max(self.game_duration - int(time.time() - self.start_time), 0)
        self.timer_surface = timer_font.render(f'Time: {self.remaining_time}', False, (211,166,139))
        return self.remaining_time == 0
    
    def update(self):
        if self.fruit.update_fruit_physics():
            self.strikes += 1
            self.fruit.reset_fruit()
        
    def draw_timer(self, screen):
        screen.blit(self.timer_surface, self.timer_rect)
        self.fruit.draw_fruit(screen)

# Initialisation
game = Game()

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        #menu
        if game.menu_state == "menu":
            if play_button.handle_event(event):
                game.menu_state = "game"
                game.reset_game()
            if quit_button.handle_event(event):
                pygame.quit()
                exit()
                
    # Background
    screen.blit(slicer_bg_surface, (0, 0))
    screen.blit(game_name_surface, game_name_rect)
    
    if game.menu_state == "menu":
        play_button.draw_button(screen)
        quit_button.draw_button(screen)
    
    elif game.menu_state == "game":

        if game.update_timer():
            game.menu_state = "menu"
            continue
        game.update()

        # Display fruit
        if game.strikes == 3:
            game.menu_state = "menu"
            continue
            
        # Draw Fruit
        game.fruit.draw_fruit(screen)

    
    # Update Display
    pygame.display.update()
    clock.tick(60)