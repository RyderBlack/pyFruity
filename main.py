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

class Fruit:
    def __init__(self):
        self.file_path = "./graphics/fruits/*.png"
        self.images = glob.glob(self.file_path)
        self.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
    def reset_fruit(self):
        # Fruits physics
        self.x = random.randint(50, WIDTH - 50)
        self.y = HEIGHT
        self.x_velocity = random.choice([-3, -2, -1, 1, 2, 3])
        self.y_velocity = -13
        self.gravity = 0.3
        
        random_image = random.choice(self.images)
        self.surface = pygame.image.load(random_image).convert_alpha()
        self.surface = pygame.transform.scale2x(self.surface)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        
        self.letter = random.choice(self.letters)
        letter_x = self.rect.x
        letter_y = self.rect.y - 30
        self.letter_surface = letter_font.render(self.letter, True, 'Red')
        self.letter_rect = self.letter_surface.get_rect(center=(letter_x,letter_y))
        
    def update_fruit_physics(self):
        self.y_velocity += self.gravity
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.rect.center = (self.x, self.y)
        self.letter_rect.x = self.rect.x
        self.letter_rect.y = self.rect.y - 30
        
        # check if fruit out of screen
        if self.y > HEIGHT:
            return True
        return False
        
    def draw_fruit(self, screen):
        screen.blit(self.surface, self.rect)
        screen.blit(self.letter_surface, self.letter_rect)

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
        self.score = 0
        
        # Timer surface
        self.timer_surface = timer_font.render(f'Time: {self.remaining_time}', False, (211,166,139))
        self.timer_rect = self.timer_surface.get_rect(topright=(WIDTH-20, 20))
        
        self.score_surface = timer_font.render(f'Score: {self.score}', False, (211,166,139))
        self.score_rect = self.score_surface.get_rect(topleft=(20, 20))
        
    def reset_game(self):
        self.strikes = 0
        self.game_over = False
        self.start_time = time.time()
        self.fruit.reset_fruit()
        self.score = 0
        
    def update_timer(self):
        self.remaining_time = max(self.game_duration - int(time.time() - self.start_time), 0)
        self.timer_surface = timer_font.render(f'Time: {self.remaining_time}', False, (211,166,139))
        return self.remaining_time == 0
    
    def update_score(self):
        self.score_surface = timer_font.render(f'Score: {self.score}', False, (211,166,139))
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            print(event.unicode.upper(),self.fruit.letter)
            if event.unicode.upper() == self.fruit.letter:
                self.score += 1
                print(f' Touché!! {self.score}')
                self.update_score()
                self.fruit.reset_fruit()
                return True
        return False
    
    def update(self):
        if self.fruit.update_fruit_physics():
            self.strikes += 1
            self.fruit.reset_fruit()
        
    def draw(self, screen):
        screen.blit(self.timer_surface, self.timer_rect)
        screen.blit(self.score_surface, self.score_rect)
        self.fruit.draw_fruit(screen)

# Initialisation Game
game = Game()

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        # Menu window
        if game.menu_state == "menu":
            if play_button.handle_event(event):
                game.menu_state = "game"
                game.reset_game()
            if quit_button.handle_event(event):
                pygame.quit()
                exit()
                
        elif game.menu_state == "game":
            game.handle_input(event)
            
    # Background
    screen.blit(slicer_bg_surface, (0, 0))
    screen.blit(game_name_surface, game_name_rect)
    
    # Menu states
    if game.menu_state == "menu":
        play_button.draw_button(screen)
        quit_button.draw_button(screen)
    
    elif game.menu_state == "game":
        if game.update_timer():
            game.menu_state = "menu"
            continue
        game.update()

        if game.strikes == 3:
            game.menu_state = "menu"
            continue
            
        # Draw fruits
        game.draw(screen)

    
    # Update Display
    pygame.display.update()
    clock.tick(60)
