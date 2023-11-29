import pygame as pg
from constantes import *
from auxiliar import SurfaceManager as sf
import sys

# BOTONES MENU PRINCIPAL
FONDO_MENU_PRINCIPAL = "background/game_background_1.png"
MENU_PRINCIPAL_TITULO = "botones/menu_principal_titulo.png"
MENU_PRINCIPAL_SELECCION_NIVEL = "botones/menu_principal_seleccion_nivel.png"
MENU_PRINCIPAL_PUNUACIONES = "botones/menu_principal_puntuaciones.png"
MENU_PRINCIPAL_SALIR = "botones/menu_principal_salir.png"

CURSOR = "botones/cursor.png"

SELECCION_NIVEL_TITULO = "botones/seleccion_nivel_titulo.png"
SELECCION_NIVEL_1 = "botones/seleccion_nivel_1.png"
SELECCION_NIVEL_2 = "botones/seleccion_nivel_2.png"
SELECCION_NIVEL_3 = "botones/seleccion_nivel_3.png"
VOLVER = "botones/volver.png"


class Cursor(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = sf.getSurfaceFromFile(CURSOR)
        self.rect = self.image.get_rect()  # Obtiene el rectángulo que rodea la imagen

    def update(self):
        # Actualiza la posición de la mira para seguir el cursor del mouse
        self.rect.center = pg.mouse.get_pos()

class Button(pg.sprite.Sprite):
    def __init__(self, sprite_rute,pos_x,pos_y,scale=1):
        super().__init__()
        self.image = sf.getSurfaceFromFile(sprite_rute,flip=False,scale=scale)
        self.rect = self.image.get_rect(x=pos_x, y=pos_y)

class MenuPrincipal:
    def __init__(self):
        #Fondo
        self.fondo = pg.transform.scale(pg.image.load(FONDO_MENU_PRINCIPAL), (ANCHO_VENTANA, ALTO_VENTANA))

        # Botones
        self.button_group = pg.sprite.Group()
        self.titulo = Button(MENU_PRINCIPAL_TITULO,75,30,scale=3.5)
        self.seleccion_nivel = Button(MENU_PRINCIPAL_SELECCION_NIVEL,210,230,scale=2)
        self.puntuaciones = Button(MENU_PRINCIPAL_PUNUACIONES,210,330,scale=2)
        self.salir = Button(MENU_PRINCIPAL_SALIR,210,430,scale=2)
        self.button_group.add(self.titulo)
        self.button_group.add(self.seleccion_nivel)
        self.button_group.add(self.puntuaciones)
        self.button_group.add(self.salir)
    
    def update(self, eventos, game):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                lista_botones = pg.sprite.spritecollide(game.cursor.sprite, self.button_group, False)
                for boton in lista_botones:
                    if boton == self.seleccion_nivel:
                        game.is_selecting_level = True
                        game.is_running_menu_principal = False
                    elif boton == self.salir:
                        pg.quit() 
                        sys.exit()

class MenuSeleccionNivel:
    def __init__(self):
        #Fondo
        self.fondo = pg.transform.scale(pg.image.load(FONDO_MENU_PRINCIPAL), (ANCHO_VENTANA, ALTO_VENTANA))

        # Botones
        self.button_group = pg.sprite.Group()
        self.titulo = Button(SELECCION_NIVEL_TITULO,75,30,scale=3.5)
        self.nivel_1 = Button(SELECCION_NIVEL_1,210,230,scale=2)
        self.nivel_2 = Button(SELECCION_NIVEL_2,210,330,scale=2)
        self.nivel_3 = Button(SELECCION_NIVEL_3,210,430,scale=2)
        self.volver = Button(VOLVER,20,500,scale=0.7)
        self.button_group.add(self.titulo)
        self.button_group.add(self.nivel_1)
        self.button_group.add(self.nivel_2)
        self.button_group.add(self.nivel_3)
        self.button_group.add(self.volver)
    
    def update(self, eventos, game):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                lista_botones = pg.sprite.spritecollide(game.cursor.sprite, self.button_group, False)
                for boton in lista_botones:
                    if boton == self.nivel_1:
                        game.level_selected = 1
                        game.is_selecting_level = False
                    elif boton == self.nivel_2:
                        game.level_selected = 2
                        game.is_selecting_level = False
                    elif boton == self.nivel_3:
                        game.level_selected = 3
                        game.is_selecting_level = False
                    elif boton == self.volver:
                        game.is_selecting_level = False
                        game.is_running_menu_principal = True
                        game.enter_menu = 0