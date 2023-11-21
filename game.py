import pygame as pg
from player import Player
from enemy import Enemy
from constantes import *

class Game:
    def __init__(self):

        # Jugador
        player = Player(0, 500, frame_rate_animation=70,frame_rate_movement=40, speed_run=10,scale=0.2)
        self.player = pg.sprite.GroupSingle(player)

        # Bullet
        self.bullet_group = pg.sprite.Group()

        # Enemys
        self.enemy_group = pg.sprite.Group()
        self.enemy_group.add(Enemy(300, 0,100,500, frame_rate_animation=150,frame_rate_movement=40, speed_run=3,scale=0.2))

    def run(self,screen,delta_ms):
        # Actualizar y Dibujar Jugador
        self.player.update(delta_ms, self.bullet_group)
        self.player.draw(screen)

        self.bullet_group.update()
        self.bullet_group.draw(screen)

        self.enemy_group.update(delta_ms, self.bullet_group,self.player)
        self.enemy_group.draw(screen)