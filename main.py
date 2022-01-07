from settings import *
import sys
import math
import time as pgt
import os
from sprites import *
from random import randint
from sprites import *

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

WIDTH = 800
HEIGHT = 600

screen = pg.display.set_mode((WIDTH, HEIGHT))
score = -500

WIDTH = 800
HEIGHT = 600
FPS = 60

pg.init()
pg.font.init()


BLACK = (0,0,0)
GREY = (50, 50, 50)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (125,125,0)

comic_sans30 = pg.font.SysFont('Comic Sans MS', 30)

speed = 1

pg.display.set_caption("Zombie Shooter")

icon = pg.image.load("icon.png")
pg.display.set_icon(icon)
 
clock = pg.time.Clock()
FPS = 120

map = Map2()
all_sprites.add(map)
car = Car2()
all_sprites.add(car)
zombie = Enemy()
all_sprites.add(zombie)
player = Player()
all_sprites.add(player)

playing = True
while playing:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
            pg.quit()

    all_sprites.update()

    hit1 = pg.sprite.groupcollide(bullets, enemies, True, True)

    while len(enemies) < 0:
        score += 100
        zombie = Enemy()
        all_sprites.add(zombie)
        enemies.add(zombie)

    text_popup_mags = comic_sans30.render('MAGS LEFT:' + str(player.mags_left), True, (WHITE))
    text_popup = comic_sans30.render('SCORE:' + str(score), True, (WHITE))
    text_ammo = comic_sans30.render('AMMO:' + str(player.ammo), True, (WHITE))
    
    screen.blit(text_popup, (10, 40))
    screen.blit(text_ammo, (10, 10))
    screen.blit(text_popup_mags, (10, 70))

    all_sprites.update()
    all_sprites.draw(screen)

    pg.display.update()

pg.quit()
