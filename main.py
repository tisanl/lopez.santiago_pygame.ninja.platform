import pygame as pg
import sys
from game import Game
from constantes import *

# Init
pg.init()

# Pantalla y fondo
screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

# Reloj
clock = pg.time.Clock()

# Juego
game = Game()

evento_1_segundo = pg.USEREVENT
pg.time.set_timer(evento_1_segundo, 1000)
paso_1_segundo = False

while True:
    lista_eventos = pg.event.get()
    for event in lista_eventos:
        if event.type == pg.QUIT:
                pg.quit() 
                sys.exit()
        if event.type == evento_1_segundo and game.is_running_level:
            game.timer.update()

    # Se actualiza el tiempo transcurrido
    delta_ms = clock.tick(FPS)
    
    if game.is_running_menu_principal:
        game.mostrar_menu_principal(screen,lista_eventos)
    
    if game.is_selecting_level:
        game.mostrar_menu_seleccion_nivel(screen,lista_eventos,delta_ms)
    
    if game.level_selected != None:
        match game.level_selected:
            case 1:
                game.nivel_1()
            case 2:
                game.nivel_2()
            case 3:
                game.nivel_3()
        game.level_selected = None
        game.is_running_level = True

    if game.is_running_level:
        game.run(screen,delta_ms)

    pg.display.update()