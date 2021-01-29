import pygame, sys
import time
import math
import random 
import math
from collections import defaultdict

pygame.init()

SCREEN_SIZE = 800, 800
NUM_BUTTER = 10
MAX_SIZE = 50
WIN = 100
SPEED = 0.01
WIN_TEXT = 'you win!' 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

collected_croissants = 0
objects = []

class Croissant:
    def __init__(self, x, y, image_file):
        self.y = y
        self.x = x

        image = pygame.image.load(image_file)
        image_size = image.get_rect().size 
        dim = image_size.index(max(image_size)) 
        scalar = 100/image_size[dim]
        new_size = [math.ceil(s*scalar) for s in image_size]
        self.image = defaultdict(
            lambda: pygame.transform.scale(image, tuple(math.ceil(s*1+MAX_SIZE/0.1) for s in new_size)),
            {i: pygame.transform.scale(image, tuple(math.ceil(s*1+i/0.1) for s in new_size)) for i in range(MAX_SIZE)})
    
class Butter:
    def __init__(self, x, y, image_file):
        self.x = x 
        self.y = y

        image = pygame.image.load(image_file)
        image_size = image.get_rect().size 
        dim = image_size.index(max(image_size)) 
        scalar = 100/image_size[dim]
        new_size = [math.ceil(s*scalar) for s in image_size]
        self.image = pygame.transform.scale(image, new_size)
    
        
screen = pygame.display.set_mode(SCREEN_SIZE)
croissant = Croissant(100, 100, "src\OuiOui.jpg")
objects.append(croissant)
for i in range(NUM_BUTTER): 
    pos = random.choice(range(SCREEN_SIZE[0])), random.choice(range(SCREEN_SIZE[1]))
    objects.append(Butter(*pos, "src\\butter.png")) 


def draw(sreen): 
    screen.fill(WHITE)
    screen.blit(objects[0].image[collected_croissants], (objects[0].x, objects[0].y))
    for obj in objects[1:]:
        screen.blit(obj.image, (obj.x, obj.y))

    font = pygame.font.SysFont(None, 24)
    text = font.render(f'butter collected: {collected_croissants}', True, BLACK) 
    screen.blit(text, (20, 20))

def draw_win_screen(screen): 
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 24)
    text = font.render(WIN_TEXT, True, BLACK) 
    text_size = font.size(WIN_TEXT)
    screen.blit(text, (SCREEN_SIZE[0]/2-text_size[0]/2, SCREEN_SIZE[1]/2-text_size[1]/2))

while 1:
    time.sleep(SPEED)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: sys.exit()

    keys = pygame.key.get_pressed()
    croissant.x += (keys[pygame.K_d] - keys[pygame.K_a]) * 5
    croissant.y += (keys[pygame.K_s] - keys[pygame.K_w]) * 5

    croissant_size = croissant.image[collected_croissants].get_rect().size
    if croissant.x < -croissant_size[0]:
        croissant.x = SCREEN_SIZE[0] + croissant_size[0]
    elif croissant.x > SCREEN_SIZE[0] + croissant_size[0]: 
        croissant.x = - croissant_size[0]
    
    if croissant.y < -croissant_size[1]: 
        croissant.y = SCREEN_SIZE[1] + croissant_size[1]
    elif croissant.y > SCREEN_SIZE[1] + croissant_size[1]:  
        croissant.y = -croissant_size[1]

    for obj in objects: 
        if obj == croissant: continue
        obj_size = obj.image.get_rect().size
        if croissant.image[collected_croissants].get_rect(topleft = (croissant.x, croissant.y)).colliderect(obj.image.get_rect(topleft=(obj.x, obj.y))): 
            collected_croissants += 1
            objects.remove(obj)

        if len(objects) == 1: 
            pos = random.choice(range(SCREEN_SIZE[0]-100)), random.choice(range(SCREEN_SIZE[1]-100))
            objects.append(Butter(*pos, "src\\butter.png")) 
    
    if collected_croissants >= WIN: 
        draw_win_screen(screen)
    else: 
        draw(screen)
    pygame.display.update()
