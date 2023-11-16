import pygame as pg
from player import Player
from constantes import *

class Game:
    def __init__(self):

        # Jugador
        player = Player(0, GROUND_LEVEL, frame_rate_animation=70,frame_rate_movement=40, speed_run=10,scale=0.2)
        self.player = pg.sprite.GroupSingle(player)

        # Bullet
        #self.bullet_group = pygame.sprite.Group()

        # Enemys
        #self.enemy_group = pygame.sprite.Group()
        #self.enemy_group.add(Enemy((10, 0),screen_w, 3))

    def run(self,screen,delta_ms):
        # Actualizar y Dibujar Jugador
        self.player.update(delta_ms)
        self.player.draw(screen)

        #self.bullet_group.update(self.enemy_group)
        #self.bullet_group.draw(screen)

        #self.enemy_group.update()
        #self.enemy_group.draw(screen)