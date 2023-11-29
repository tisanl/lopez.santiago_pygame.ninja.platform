import pygame as pg
from constantes import *
from auxiliar import SurfaceManager as sf

HEART_SPRITE = "items_sprites/heart_0.png"
EMPTY_HEART_SPRITE = "items_sprites/heart_1.png"

COIN_TWIST = "items_sprites/coin_0{0}.png"


class Heart(pg.sprite.Sprite):
    def __init__(self,pos_x,pos_y,empty=False,scale=1):
        super().__init__()
        if empty:
            self.image = sf.getSurfaceFromFile(EMPTY_HEART_SPRITE,flip=False,scale=scale)
        else:
            self.image = sf.getSurfaceFromFile(HEART_SPRITE,flip=False,scale=scale)

        self.rect = self.image.get_rect(x=pos_x, y=pos_y)

class Coin(pg.sprite.Sprite):
    def __init__(self,pos_x,pos_y,frame_rate_animation=150,scale=1):
        super().__init__()
        self.__animation = sf.getSurfaceFromSeparateFiles(COIN_TWIST,0,2,flip=False,scale=scale)

        self.__frame = 0                                            # Frame actual de la animacion que se esta reproduciendo. Se inicializa en 0
        self.image = self.__animation[self.__frame]
        self.__frame_rate_animation = frame_rate_animation          # Variable que guarda la velocidad con la que se cambia la imagen
        self.__coin_animation_time = 0

        self.rect = self.image.get_rect(x=pos_x, y=pos_y)

    def update(self, delta_ms):
        self.__coin_animation_time += delta_ms
        if self.__coin_animation_time >= self.__frame_rate_animation:
            self.__coin_animation_time = 0
            if self.__frame < len(self.__animation) - 1:
                self.__frame += 1
            else:
                self.__frame = 0
            self.image = self.__animation[self.__frame]