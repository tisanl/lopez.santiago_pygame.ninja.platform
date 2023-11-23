import pygame as pg
from player import Player
from enemy import Enemy
from constantes import *
from auxiliar import SurfaceManager as sf
from gui import Cursor
from gui import MenuSeleccionNivel
from gui import MenuPrincipal

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

        # Menus
        self.is_running_menu_principal = True
        self.is_running_level = False
        self.is_selecting_level = False
        self.level_selected = None
        self.is_running_image_post_level = False
        
        self.enter_menu = 0
        self.cooldown_menus = 100

        self.menu_principal = MenuPrincipal()
        self.menu_seleccion_nivel = MenuSeleccionNivel()
        self.cursor = pg.sprite.GroupSingle(Cursor())

    def run(self,screen,delta_ms):
        # Actualizar y Dibujar Jugador
        screen.blit(self.menu_principal.fondo, self.menu_principal.fondo.get_rect())
        pg.mouse.set_visible(True)

        self.player.update(delta_ms, self.bullet_group)
        self.player.draw(screen)

        self.bullet_group.update()
        self.bullet_group.draw(screen)

        self.enemy_group.update(delta_ms, self.bullet_group,self.player)
        self.enemy_group.draw(screen)

    def mostrar_menu_principal(self, screen, eventos):
        pg.mouse.set_visible(False)
        self.cursor.update()
        self.menu_principal.update(eventos, self)
        
        screen.blit(self.menu_principal.fondo, self.menu_principal.fondo.get_rect())
        self.menu_principal.button_group.draw(screen)
        self.cursor.draw(screen)
    
    def mostrar_menu_seleccion_nivel(self, screen, eventos, delta_ms):
        pg.mouse.set_visible(False)
        self.cursor.update()
        self.enter_menu += delta_ms
        if self.enter_menu >= self.cooldown_menus:
            self.menu_seleccion_nivel.update(eventos, self)
        
        screen.blit(self.menu_principal.fondo, self.menu_principal.fondo.get_rect())
        self.menu_seleccion_nivel.button_group.draw(screen)
        self.cursor.draw(screen)
        
        
        
