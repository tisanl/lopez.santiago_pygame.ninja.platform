import pygame as pg
from constantes import *
from auxiliar import SurfaceManager as sf

class Bullet(pg.sprite.Sprite):
    def __init__(self, sprite_rute,pos_x,pos_y,speed,looking_right,scale=1):
        super().__init__()
        if looking_right:
            self.image = sf.getSurfaceFromFile(sprite_rute,flip=False,scale=scale)
        else:
            self.image = sf.getSurfaceFromFile(sprite_rute,flip=True,scale=scale)
        self.rect = self.image.get_rect(x=pos_x, y=pos_y)
        self.is_looking_right = looking_right
        self.speed = speed
    
    def update(self):
        if self.is_looking_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        if self.rect.x >= ANCHO_VENTANA or self.rect.x <= 0:
            self.kill()
        #pygame.sprite.spritecollide(self, enemy_group, True)