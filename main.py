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
        if event.type == evento_1_segundo and game.is_running == RUNNING_GAME:
            game.timer.update()
        if pg.key.get_pressed()[pg.K_p] and game.is_running == RUNNING_GAME:
            game.is_running = MENU_PAUSA

    # Se actualiza el tiempo transcurrido
    delta_ms = clock.tick(FPS)
    
    match game.is_running:
        case "Menu Principal":
            game.mostrar_menu_principal(screen,lista_eventos)
        case "Menu Seleccion de Nivel":
            game.mostrar_menu_seleccion_nivel(screen,lista_eventos,delta_ms)
            if game.level_selected != None:
                game.is_running = RUNNING_GAME
        case "Juego":
            game.run(screen,delta_ms)
        case "Post Game":
            game.mostrar_menu_post_game(screen,lista_eventos,delta_ms)
        case "En Pausa":
            game.mostrar_menu_pausa(screen,lista_eventos,delta_ms)
    
    pg.display.update()