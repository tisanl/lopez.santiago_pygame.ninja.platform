import pygame as pg
from player import Player
from enemy import Enemy_Bug
from enemy import Enemy_Alien
from constantes import *
from auxiliar import SurfaceManager as sf
from gui import Cursor
from gui import MenuSeleccionNivel
from gui import MenuPrincipal
from platforms import Platform
from platforms import Marco
from items import Coin
from marcadores import MarcadorTiempo

MURO_PIEDRA = "platform_sprites/muro_piedra.png"
PISO_PIEDRA = "platform_sprites/piso_piedra.png"
NUBE_IZQUIERDA = "platform_sprites/nube_izquierda.png"
NUBE_DERECHA = "platform_sprites/nube_derecha.png"
NUBE_CENTRO = "platform_sprites/nube_medio.png"

class Game:
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  INIT DEL JUEGO  --------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def __init__(self):
        # Variables controladoras de que es lo que se esta ejecutando
        self.is_running_menu_principal = True       # Si se esta ejecutando el menu principal
        self.is_selecting_level = False             # Si se esta ejecutando el menu de seleccion de nivel
        self.level_selected = None                  # Esta variable guarda si hay algun nivel seleccionado
        self.is_running_level = False               # Si se esta ejecutando un nivel
        self.is_running_image_post_level = False    # Si se esta ejecutando el menu post nivel

        # Variables que guardan los objetos del Nivel mientras se esta corriendo
        self.player = pg.sprite.GroupSingle()       # Jugador, grupo Simple
        self.enemy_group = pg.sprite.Group()        # Enemys, grupo
        self.marco = pg.sprite.Group()              # Variable que guarda los objetos del Marco del nivel (plataformas)
        self.platform_group = pg.sprite.Group()     # Platforms, grupo que guarda las plataformas propias del nivel
        self.bullet_group = pg.sprite.Group()
        self.coin_group = pg.sprite.Group()
        
        # Variables Auxiliares
        self.enter_menu = 0             # Variable que guarda el tiempo de cuando se entro al menu
        self.cooldown_menus = 100       # Variable que pone un cooldawn para poder empezar a interactuar con el menu

        self.menu_principal = MenuPrincipal()
        self.menu_seleccion_nivel = MenuSeleccionNivel()
        self.cursor = pg.sprite.GroupSingle(Cursor())

        self.timer = None

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ------------------------------------------------------  FUNCIONES DE GUI  ---------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
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
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  FUNCIONES DE NIVEL  ----------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def run(self,screen,delta_ms):
        # Actualizar y Dibujar Jugador
        pg.mouse.set_visible(True)
        screen.blit(self.menu_principal.fondo, self.menu_principal.fondo.get_rect())

        # Se actualizan y dibujan las monedas
        self.coin_group.update(delta_ms)
        self.coin_group.draw(screen)

        # Se actualizan y dibujan enemigos
        self.enemy_group.update(delta_ms,self.player)
        self.enemy_group.draw(screen)

        for enemy in self.enemy_group:              # Por cada enemigo
            if enemy.is_shooter:                    # Si dispara
                enemy.bullet_group.draw(screen)     # Dibuja el grupo de balas enemigas
                #pg.draw.rect(screen, 'green', enemy.shooting_colition_rect)

        # Se upgradea y dibuja al player
        self.player.update(delta_ms,self.platform_group, self.enemy_group, self.coin_group)
        self.player.draw(screen)
        self.player.sprite.bullet_group.draw(screen)            # Se dibuja su grupo de balas
        self.player.sprite.marcador_puntuacion.draw(screen)     # Se dibuja el marcoador de puntuacion
        self.player.sprite.lives_group.draw(screen)             # Se dibuja las vidas del jugador

        # Se dibuja el timer del juego
        self.timer.draw(screen)

        # Se sibuja el entorno, plataformas y el marco
        self.platform_group.draw(screen)
        self.marco.draw(screen)
        
        #for platform in self.platform_group:
            #pg.draw.rect(screen, 'red', platform.rect_platform)
            #pg.draw.rect(screen, 'green', platform.rect)

        #if False:
            #pg.draw.rect(screen, 'red', self.player.sprite.player_foot)
            #pg.draw.rect(screen, 'red', self.player.sprite.player_side_right)
            #pg.draw.rect(screen, 'red', self.player.sprite.player_side_left)

    def nivel_1(self):
        # Marco
        self.marco = Marco().platform_group
        
        # Player
        player = Player(50, 420, frame_rate_animation=50,frame_rate_movement=40, speed_run=10,scale=0.15)
        self.player = pg.sprite.GroupSingle(player)

        # Plataformas
        # Piedra
        for i in range(1, 12):
            x = 0 + 36 * i
            self.platform_group.add(Platform(PISO_PIEDRA,x,200,is_platform=True,scale=2))
            self.platform_group.add(Platform(MURO_PIEDRA,x,230,scale=2))
            self.platform_group.add(Platform(MURO_PIEDRA,x,254,scale=2))

        # Nubes
        nubes = [{"largo" : 2, "x": 656, "y" : 100},
                {"largo" : 3, "x": 476, "y" : 190},
                {"largo" : 3, "x": 620, "y" : 280},
                {"largo" : 4, "x": 440, "y" : 350}]
        
        for nube in nubes:
            self.platform_group.add(Platform(NUBE_IZQUIERDA,nube["x"],nube["y"],transparent=True,is_platform=True,scale=2))
            for i in range(1, nube["largo"]):
                x = nube["x"] + 36 * i
                if i != nube["largo"] -1:
                    self.platform_group.add(Platform(NUBE_CENTRO,x,nube["y"],transparent=True,is_platform=True,scale=2))
                else:
                    self.platform_group.add(Platform(NUBE_DERECHA,x,nube["y"],transparent=True,is_platform=True,scale=2))
        
        # Enemigos
        self.enemy_group.add(Enemy_Bug(500, GROUND_LEVEL, True, limit_left=400,limit_right=750, frame_rate_animation=400,frame_rate_movement=50, speed_walk=3,scale=2))
        self.enemy_group.add(Enemy_Alien(50, 200, True, frame_rate_animation=400,scale=2))

        # Monedas
        monedas = [{"largo": 5, "x" : 50, "y" : 320, "salteo" : True, "espacio" : 80},
                    {"largo": 4, "x" : 90, "y" : 85, "salteo" : False, "espacio" : 80},
                    {"largo": 1, "x" : 675, "y" : 50, "salteo" : False, "espacio" : 36},
                    {"largo": 1, "x" : 660, "y" : 370, "salteo" : False, "espacio" : 80},
                    {"largo": 1, "x" : 660, "y" : 200, "salteo" : False, "espacio" : 36}]
        
        for grupo in monedas:
            for i in range(grupo["largo"]):
                x = grupo["x"] + grupo["espacio"] * i
                if grupo["salteo"]:
                    if i % 2 == 0:
                        self.coin_group.add(Coin(x,grupo["y"],scale=2))
                    else:
                        self.coin_group.add(Coin(x,grupo["y"]-30,scale=2))
                else:
                    self.coin_group.add(Coin(x,grupo["y"],scale=2))
        
        self.timer = MarcadorTiempo(3,140,36,20)

    
    def nivel_2(self):
        # Marco
        self.marco = Marco().platform_group
        
        # Player
        player = Player(50, 300, frame_rate_animation=50,frame_rate_movement=50, speed_run=10,jump=3,gravity=3,jump_max_high=500,scale=0.15)
        self.player = pg.sprite.GroupSingle(player)
    
    def nivel_3(self):
        # Marco
        self.marco = Marco().platform_group
        
        # Player
        player = Player(50, 300, frame_rate_animation=50,frame_rate_movement=40, speed_run=10,scale=0.15)
        self.player = pg.sprite.GroupSingle(player)

        # Enemigos
        enemy = Enemy_Bug(500, GROUND_LEVEL, limit_left=400,limit_right=600, frame_rate_animation=50,frame_rate_movement=40, speed_walk=3,scale=2)
        self.enemy_group.add(enemy)
    


        
        
