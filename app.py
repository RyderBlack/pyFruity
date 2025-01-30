import pygame
import glob, random
from sys import exit

WIDTH, HEIGHT = 800,450

class Fruit:
    def __init__(self, fruit_images):
        # Load random fruit image
        self.image = pygame.image.load(random.choice(fruit_images)).convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        
        # Initial position and velocity
        self.x = random.randint(50, WIDTH - 50)
        self.y = HEIGHT
        self.x_velocity = random.choice([-3, -2, -1, 1, 2, 3])
        self.y_velocity = -15
        self.gravity = 0.5
        
    def update(self):
        # Update position and velocity
        self.y_velocity += self.gravity
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.rect.center = (self.x, self.y)
        
    def is_off_screen(self):
        return self.y > HEIGHT + 50

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pixel Fruit Slicer')
clock = pygame.time.Clock()

# Load all fruit images
fruit_images = glob.glob("./graphics/fruits/*.png")

# Create Text and font
my_main_font = pygame.font.Font('fonts/Pixeltype.ttf', 80)

# Environment
slicer_bg_surface = pygame.image.load('graphics/environments/slicer_bg.png').convert()

# Game name
game_name_surface = my_main_font.render('Pixel Fruit Slicer', False, (211,166,139))
game_name_rect = game_name_surface.get_rect(center=(400,80))

# Game Variables
fruits = []  # List to store active fruits
spawn_timer = 0
SPAWN_INTERVAL = 60  # Adjust this to control fruit spawn rate
strikes = 0
game_over = False
score = 0

# Main Game Loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # Spawn new fruits
    spawn_timer += 1
    if spawn_timer >= SPAWN_INTERVAL:
        fruits.append(Fruit(fruit_images))
        spawn_timer = 0
    
    # Background
    screen.blit(slicer_bg_surface, (0, 0))
    screen.blit(game_name_surface, game_name_rect)
    
    # Update and draw fruits
    for fruit in fruits:  # Use slice copy to safely remove fruits
        fruit.update()
        
        # Check if fruit is off screen
        if fruit.is_off_screen():
            fruits.remove(fruit)
            strikes += 1
            if strikes == 3:
                game_over = True
        else:
            screen.blit(fruit.image, fruit.rect)
    
    # Draw score and strikes
    score_text = my_main_font.render(f'Score: {score}', False, (211,166,139))
    strikes_text = my_main_font.render(f'Strikes: {strikes}', False, (211,166,139))
    screen.blit(score_text, (20, 20))
    screen.blit(strikes_text, (20, 60))
    
    pygame.display.update()
    clock.tick(60)

# Game Over screen
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill((0, 0, 0))
    game_over_text = my_main_font.render(f'Game Over! Score: {score}', False, (255,255,255))
    game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(game_over_text, game_over_rect)
    
    pygame.display.update()
    clock.tick(60)