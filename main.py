import pygame as pg
import sys
from game import Game
from constantes import *

# Init
pg.init()

# Pantalla y fondo
screen = pg.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
back_img = pg.image.load('C:/Users/Usuario/Desktop/Proyecto Final/Proyecto Final/background/game_background_1.png')
back_img = pg.transform.scale(back_img, (ANCHO_VENTANA, ALTO_VENTANA))

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
    
    # Se actualiza el juego y se dibuja
    screen.blit(back_img, back_img.get_rect())
    game.run(screen,delta_ms)

    pg.display.update()
