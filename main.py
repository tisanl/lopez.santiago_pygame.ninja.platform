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

while True:
    lista_eventos = pg.event.get()
    for event in lista_eventos:
        if event.type == pg.QUIT:
                pg.quit() 
                sys.exit()

    # Se actualiza el tiempo transcurrido
    delta_ms = clock.tick(FPS)
    
    if game.is_running_menu_principal:
        game.mostrar_menu_principal(screen,lista_eventos)
    
    if game.is_selecting_level:
        game.mostrar_menu_seleccion_nivel(screen,lista_eventos,delta_ms)
    
    if game.level_selected != None:
        game.run(screen,delta_ms)

    pg.display.update()