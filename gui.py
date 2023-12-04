import pygame as pg
from constantes import *
from auxiliar import SurfaceManager as sf
import sys

# CURSOR
CURSOR = "gui_sprites/cursor.png"

# BOTONES MENU PRINCIPAL
FONDO_MENU_PRINCIPAL = "background/game_background_1.png"
MENU_PRINCIPAL_TITULO = "gui_sprites/menu_principal/titulo.png"
MENU_PRINCIPAL_SELECCION_NIVEL = "gui_sprites/menu_principal/seleccion_nivel.png"
MENU_PRINCIPAL_PUNUACIONES = "gui_sprites/menu_principal/puntuaciones.png"
MENU_PRINCIPAL_SALIR = "gui_sprites/menu_principal/salir.png"

# BOTONES SELECCION DE NIVEL
SELECCION_NIVEL_TITULO = "gui_sprites/seleccion_nivel/titulo.png"
SELECCION_NIVEL_1 = "gui_sprites/seleccion_nivel/nivel_1.png"
SELECCION_NIVEL_2 = "gui_sprites/seleccion_nivel/nivel_2.png"
SELECCION_NIVEL_3 = "gui_sprites/seleccion_nivel/nivel_3.png"

# BOTONES SELECCION DE NIVEL
POST_GAME_FONDO = "gui_sprites/post_game/back.png"
POST_GAME_VICTORY = "gui_sprites/post_game/victory_title.png"
POST_GAME_DEFEATED = "gui_sprites/post_game/defeat_title.png"
POST_GAME_REPLAY = "gui_sprites/post_game/volver_a_jugar.png"
POST_GAME_SAFE_POINTS = "gui_sprites/post_game/safe_puntuacion.png"

# BOTONES PAUSA
PAUSA_TITULO = "gui_sprites/pause/title.png"
PAUSA_REINICIAR = "gui_sprites/pause/reiniciar_nivel.png"
PAUSA_CONTINUAR = "gui_sprites/pause/continuar.png"

# GENERALES
VOLVER = "gui_sprites/generales/volver_atras.png"
BACK_MENU_PRINCIPAL = "gui_sprites/generales/back_menu_principal.png"
BACK_SELECCION_NIVEL = "gui_sprites/generales/back_level_selection.png"


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
                        game.is_running = MENU_SELECCION
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
                        game.nivel_1()
                    elif boton == self.nivel_2:
                        game.level_selected = 2
                        game.nivel_2()
                    elif boton == self.nivel_3:
                        game.level_selected = 3
                        game.nivel_3()
                    elif boton == self.volver:
                        game.is_running = MENU_PRINCIPAL
                        game.enter_menu = 0

class MenuPostGame:
    def __init__(self,win:bool):
        #Fondo
        
        self.fondo = pg.transform.scale(pg.image.load(POST_GAME_FONDO), ((ANCHO_VENTANA/6)*4.5, (ALTO_VENTANA/6)*4.5))
        x = ((ANCHO_VENTANA - self.fondo.get_width()) // 2)
        y = ((ALTO_VENTANA - self.fondo.get_height()) // 2)
        self.fondo_rect = self.fondo.get_rect(x=x, y=y)

        # Botones
        self.button_group = pg.sprite.Group()
        if win:
            self.titulo = Button(POST_GAME_VICTORY,x+90,y+30,scale=2.2)
        else:
            self.titulo = Button(POST_GAME_DEFEATED,x+90,y+30,scale=2.2)
        separacion_x = 180
        separacion_y = 65
        y_comienzo_botones = 220
        self.replay = Button(POST_GAME_REPLAY,x+separacion_x,y_comienzo_botones,scale=1.3)
        self.safe_points = Button(POST_GAME_SAFE_POINTS,x+separacion_x,y_comienzo_botones+separacion_y,scale=1.3)
        self.back_menu_seleccion_nivel = Button(BACK_SELECCION_NIVEL,x+separacion_x,y_comienzo_botones+separacion_y*2,scale=1.3)
        self.back_menu_principal = Button(BACK_MENU_PRINCIPAL,x+separacion_x,y_comienzo_botones+separacion_y*3,scale=1.3)
        self.button_group.add(self.titulo)
        self.button_group.add(self.replay)
        self.button_group.add(self.safe_points)
        self.button_group.add(self.back_menu_seleccion_nivel)
        self.button_group.add(self.back_menu_principal)
    
    def update(self, eventos, game):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                lista_botones = pg.sprite.spritecollide(game.cursor.sprite, self.button_group, False)
                for boton in lista_botones:
                    if boton == self.replay:
                        game.is_running = RUNNING_GAME
                        match game.level_selected:
                            case 1:
                                game.nivel_1()
                            case 2:
                                game.nivel_2()
                            case 3:
                                game.nivel_3()
                    elif boton == self.back_menu_principal:
                        game.is_running = MENU_PRINCIPAL
                        game.level_selected = None
                        game.enter_menu = 0
                    elif boton == self.back_menu_seleccion_nivel:
                        game.is_running = MENU_SELECCION
                        game.level_selected = None
                        game.enter_menu = 0
        
class MenuPausa:
    def __init__(self):
        #Fondo
        
        self.fondo = pg.transform.scale(pg.image.load(POST_GAME_FONDO), ((ANCHO_VENTANA/6)*4.5, (ALTO_VENTANA/6)*4.5))
        x = ((ANCHO_VENTANA - self.fondo.get_width()) // 2)
        y = ((ALTO_VENTANA - self.fondo.get_height()) // 2)
        self.fondo_rect = self.fondo.get_rect(x=x, y=y)

        # Botones
        self.button_group = pg.sprite.Group()
        self.titulo = Button(PAUSA_TITULO,x+90,y+30,scale=2.2)
        separacion_x = 180
        separacion_y = 65
        y_comienzo_botones = 220
        self.volver_al_juego = Button(PAUSA_CONTINUAR,x+separacion_x,y_comienzo_botones,scale=1.3)
        self.replay = Button(PAUSA_REINICIAR,x+separacion_x,y_comienzo_botones+separacion_y,scale=1.3)
        self.back_menu_seleccion_nivel = Button(BACK_SELECCION_NIVEL,x+separacion_x,y_comienzo_botones+separacion_y*2,scale=1.3)
        self.back_menu_principal = Button(BACK_MENU_PRINCIPAL,x+separacion_x,y_comienzo_botones+separacion_y*3,scale=1.3)
        self.button_group.add(self.titulo)
        self.button_group.add(self.volver_al_juego)
        self.button_group.add(self.replay)
        self.button_group.add(self.back_menu_seleccion_nivel)
        self.button_group.add(self.back_menu_principal)
    
    def update(self, eventos, game):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                lista_botones = pg.sprite.spritecollide(game.cursor.sprite, self.button_group, False)
                for boton in lista_botones:
                    if boton == self.volver_al_juego:
                        game.is_running = RUNNING_GAME
                    if boton == self.replay:
                        game.is_running = RUNNING_GAME
                        match game.level_selected:
                            case 1:
                                game.nivel_1()
                            case 2:
                                game.nivel_2()
                            case 3:
                                game.nivel_3()
                    elif boton == self.back_menu_principal:
                        game.is_running = MENU_PRINCIPAL
                        game.level_selected = None
                        game.enter_menu = 0
                    elif boton == self.back_menu_seleccion_nivel:
                        game.is_running = MENU_SELECCION
                        game.level_selected = None
                        game.enter_menu = 0