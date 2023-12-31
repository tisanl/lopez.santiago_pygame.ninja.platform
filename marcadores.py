import pygame as pg
from constantes import *

class MarcadorTiempo:
    def __init__(self, minutos, segundos,pos_x, pos_y,size=10):
        self.__minutos = minutos
        self.__segundos = segundos
        
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__font = pg.font.Font(FONT, size)

        texto = "{0}:{1}".format(str(self.__minutos).zfill(2), str(0).zfill(2))
        self.__text = self.__font.render(texto, True, "white")
        self.__pos = (self.__pos_x, self.__pos_y)

        self.is_over = False

    def update(self):
        if self.__minutos == 0 and self.__segundos == 0:
            self.is_over = True
        else:
            if self.__segundos == 0:
                self.__minutos -= 1
                self.__segundos = 60
            self.__segundos -= 1
            texto = "{0}:{1}".format(str(self.__minutos).zfill(2), str(self.__segundos).zfill(2))
            self.__text = self.__font.render(texto, True, "white")
    
    def draw(self,screen):
        screen.blit(self.__text, self.__pos)

class MarcadorPuntuacion:
    def __init__(self, puntuacion, pos_x, pos_y,size=10):
        self.__puntuacion = puntuacion
        
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__font = pg.font.Font(FONT, size)

        texto = "{0}".format(str(self.__puntuacion).zfill(6))
        self.__text = self.__font.render(texto, True, "white")
        self.__pos = (self.__pos_x, self.__pos_y)

    def update(self, puntuacion):
        texto = "{0}".format(str(puntuacion).zfill(6))
        self.__text = self.__font.render(texto, True, "white")
        self.__pos = (self.__pos_x, self.__pos_y)
    
    def draw(self,screen):
        screen.blit(self.__text, self.__pos)