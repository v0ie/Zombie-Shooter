
import pygame as pg
from settings import *
import os
import time
import math
import array
import pygame.locals as pglocal
from random import randint
vec = pg.math.Vector2

pg.init()

pg.mixer.init()

rawArr=[]
for i in range(41000):
    freq1=int(math.sin(i/220.0*math.pi*2)*32767.0)
    if i>40900: freq1=int(freq1*(41000-i)/100.0) #Solution - see Final Solution
    rawArr.append(freq1)

sndArr=array.array('h',rawArr)

snd=pg.mixer.Sound(sndArr)


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

player_image_upgrade1 = ("")
ammobox = pg.image.load("ammobox.png")
no_bullets = pg.mixer.Sound("nobullet.wav")
bullet_sound = pg.mixer.Sound("bullet1soundeffect.wav")
enemy_image = pg.image.load("skeleton-idle_81.png")
player_image = pg.image.load("player2.png")
bullet_image = pg.image.load("bullet.png")
angle = 90

class Ammobox(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = ammobox
        self.image = pg.transform.scale(self.image, (100, 100))
        self.pos = vec(500, 500)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = player_image
        self.image = pg.transform.scale(self.image, (50, 50))
        self.pos = vec(500, 500)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.speed = 1
        self.speed_y = 0
        self.image_up = pg.transform.rotate(self.image, 90)
        self.image_d = pg.transform.rotate(self.image, -90,)
        self.image_lr = pg.transform.flip(self.image, True, False)
        self.image_rl = self.image
        self.direction = "RIGHT"
        self.ammo = 60
        self.last_shot = 0

    def update(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_r]:
            self.ammo = 60

        if keys[pg.K_w]:
            self.image = self.image_up
            self.pos.y -= self.speed
            self.direction = "UP"

        if keys[pg.K_s]:
            self.image = self.image_d
            self.pos.y += self.speed
            self.direction = "DOWN"

        if keys[pg.K_a]:
            self.image = self.image_lr
            self.pos.x -= self.speed
            self.direction = "LEFT"

        if keys[pg.K_d]:
            self.image = self.image_rl
            self.pos.x += self.speed
            self.direction = "RIGHT"

        if keys[pg.K_SPACE]:
            self.shoot()

        self.rect.center = self.pos
    
    def shoot(self):
        self.now = pg.time.get_ticks()
        self.now -= self.last_shot
        if self.now > 200:
            if self.ammo > 0:
                self.last_shot = pg.time.get_ticks()
                self.ammo -= 1
                bullet_sound.play()
                attack = Bullet1(self.pos.x, self.pos.y, self.direction)
                bullets.add(attack)
                all_sprites.add(attack)

            else:
                self.last_shot = pg.time.get_ticks()
                no_bullets.play()
            
class Bullet1(pg.sprite.Sprite):    
    def __init__(self, x, y, direction):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.image = pg.transform.scale(self.image, (20, 20))

        if direction == "RIGHT":
            self.pos = vec(x + 100, y + 78)

        if direction == "LEFT":
            self.pos = vec(x + 0, y + 77)
        
        if direction == "UP":
            self.pos = vec(x - -75, y - 20)
        
        if direction == "DOWN":
            self.pos = vec(x + 27, y + 120)

        self.rect.center = self.pos
        self.speed_x = 0
        self.speed_y = 0
        self.image_up = pg.transform.rotate(self.image, 90)
        self.image_down = pg.transform.rotate(self.image, -90)
        self.image_lr = pg.transform.flip(self.image, False, True)
        self.image_rl = self.image

        if direction == "UP":
            self.image = self.image_rl
            self.speed_x = 0
            self.speed_y = -10

        if direction == "DOWN":
            self.image = self.image_lr
            self.speed_x = 0
            self.speed_y = 10

        if direction == "RIGHT":
            self.image = self.image_down
            self.speed_x = 10
            self.speed_y = 0

        if direction == "LEFT":
            self.image = self.image_up
            self.speed_x = -10
            self.speed_y = 0

    def update(self):
        self.pos.x += self.speed_x
        self.pos.y += self.speed_y
        self.rect.center = self.pos



class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = enemy_image
        self.image = pg.transform.scale(self.image, (50, 50))
        self.pos = vec(-100,randint(100, 500))
        self.health = 100
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hp = 100
        self.speed_x = 1
        self.speed_back = 1
        self.speed_y = 0 
        self.image_r = self.image
        self.image_l = pg.transform.flip(self.image, True, False)
        self.image_up = pg.transform.rotate(self.image, 90)
        self.image_down = pg.transform.rotate(self.image, -90)


    def update(self):
        global enemy_image
        self.pos.x += self.speed_x
        self.pos.y += self.speed_y
        self.rect.center = self.pos

        if self.pos.x > 750:
            self.speed_x = -4
            self.speed_y = 0

            self.image = self.image_l

        elif self.pos.x < 75:
            self.speed_x = 4
            self.speed_y = 0

            self.image = self.image_r

        self.rect.center = self.pos