import pygame as pg
from player import Player
from enemy import Enemy_Bug
from enemy import Enemy_Alien
from enemy import Enemy_Block
from enemy import Enemy_Spikes
from constantes import *
from auxiliar import SurfaceManager as sf
from gui import Cursor
from gui import MenuSeleccionNivel
from gui import MenuPrincipal
from gui import MenuPostGame
from gui import MenuPausa
from gui import MenuSonido
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
        self.is_running = MENU_PRINCIPAL
        self.level_selected = None                  # Esta variable guarda si hay algun nivel seleccionado
        self.was_running = MENU_PRINCIPAL

        # Variables que guardan los objetos del Nivel mientras se esta corriendo
        self.player = pg.sprite.GroupSingle()       # Jugador, grupo Simple
        self.enemy_group = pg.sprite.Group()        # Enemys, grupo
        self.marco = pg.sprite.Group()              # Variable que guarda los objetos del Marco del nivel (plataformas)
        self.platform_group = pg.sprite.Group()     # Platforms, grupo que guarda las plataformas propias del nivel
        self.coin_group = pg.sprite.Group()
        
        # Variables Auxiliares
        self.enter_menu = 0             # Variable que guarda el tiempo de cuando se entro al menu
        self.cooldown_menus = 100       # Variable que pone un cooldawn para poder empezar a interactuar con el menu

        self.menu_principal = MenuPrincipal()
        self.menu_seleccion_nivel = MenuSeleccionNivel()
        self.menu_post_game = None
        self.menu_pausa = MenuPausa()
        self.menu_sonido = MenuSonido()
        self.cursor = pg.sprite.GroupSingle(Cursor())

        self.timer = None

        # Sonido
        self.volume = 0.1

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
    
    def mostrar_menu_post_game(self, screen, eventos, delta_ms):
        pg.mouse.set_visible(False)
        self.cursor.update()
        self.enter_menu += delta_ms
        if self.enter_menu >= self.cooldown_menus:
            self.menu_post_game.update(eventos, self)
        
        # Ultimas imagenes del juego
        screen.blit(self.menu_principal.fondo, self.menu_principal.fondo.get_rect())
        self.coin_group.draw(screen)
        self.enemy_group.draw(screen)
        for enemy in self.enemy_group:              # Por cada enemigo
            if enemy.is_shooter:                    # Si dispara
                enemy.bullet_group.draw(screen)
        self.player.draw(screen)
        self.player.sprite.bullet_group.draw(screen)            # Se dibuja su grupo de balas
        self.player.sprite.marcador_puntuacion.draw(screen)     # Se dibuja el marcoador de puntuacion
        self.player.sprite.lives_group.draw(screen)
        self.timer.draw(screen)
        self.platform_group.draw(screen)
        self.marco.draw(screen)

        screen.blit(self.menu_post_game.fondo, self.menu_post_game.fondo_rect)
        self.menu_post_game.button_group.draw(screen)
        self.cursor.draw(screen)

    def mostrar_menu_pausa(self, screen, eventos, delta_ms):
        pg.mouse.set_visible(False)
        self.cursor.update()
        self.enter_menu += delta_ms
        if self.enter_menu >= self.cooldown_menus:
            self.menu_pausa.update(eventos, self)
        
        # Ultimas imagenes del juego
        screen.blit(self.menu_principal.fondo, self.menu_principal.fondo.get_rect())
        self.coin_group.draw(screen)
        self.enemy_group.draw(screen)
        for enemy in self.enemy_group:              # Por cada enemigo
            if enemy.is_shooter:                    # Si dispara
                enemy.bullet_group.draw(screen)
        self.player.draw(screen)
        self.player.sprite.bullet_group.draw(screen)            # Se dibuja su grupo de balas
        self.player.sprite.marcador_puntuacion.draw(screen)     # Se dibuja el marcoador de puntuacion
        self.player.sprite.lives_group.draw(screen)
        self.timer.draw(screen)
        self.platform_group.draw(screen)
        self.marco.draw(screen)

        screen.blit(self.menu_pausa.fondo, self.menu_pausa.fondo_rect)
        self.menu_pausa.button_group.draw(screen)
        self.cursor.draw(screen)
    
    def mostrar_menu_sonido(self, screen, eventos, delta_ms):
        pg.mouse.set_visible(False)
        self.cursor.update()
        self.enter_menu += delta_ms
        if self.enter_menu >= self.cooldown_menus:
            self.menu_sonido.update(eventos, self, delta_ms)
        
        if self.was_running == MENU_PAUSA:
            # Ultimas imagenes del juego
            screen.blit(self.menu_principal.fondo, self.menu_principal.fondo.get_rect())
            self.coin_group.draw(screen)
            self.enemy_group.draw(screen)
            for enemy in self.enemy_group:              # Por cada enemigo
                if enemy.is_shooter:                    # Si dispara
                    enemy.bullet_group.draw(screen)
            self.player.draw(screen)
            self.player.sprite.bullet_group.draw(screen)            # Se dibuja su grupo de balas
            self.player.sprite.marcador_puntuacion.draw(screen)     # Se dibuja el marcoador de puntuacion
            self.player.sprite.lives_group.draw(screen)
            self.timer.draw(screen)
            self.platform_group.draw(screen)
            self.marco.draw(screen)
        else:
            screen.blit(self.menu_principal.fondo, self.menu_principal.fondo.get_rect())
            self.menu_principal.button_group.draw(screen)

        screen.blit(self.menu_sonido.fondo, self.menu_sonido.fondo_rect)
        self.menu_sonido.button_group.draw(screen)
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
            #pg.draw.rect(screen, 'green', enemy.attacking_colition_rect)

        # Se upgradea y dibuja al player
        self.player.update(delta_ms,self.platform_group, self.enemy_group, self.coin_group)
        self.player.draw(screen)
        self.player.sprite.bullet_group.draw(screen)            # Se dibuja su grupo de balas

        # Se sibuja el entorno, plataformas y el marco
        self.platform_group.draw(screen)
        self.marco.draw(screen)

        # Se dibuja el timer del juego, vida y puntaje
        self.player.sprite.marcador_puntuacion.draw(screen)     # Se dibuja el marcoador de puntuacion
        self.player.sprite.lives_group.draw(screen)             # Se dibuja las vidas del jugador
        self.timer.draw(screen)

        if self.timer.is_over or self.player.sprite.lives_actual <= 0:
            self.is_running = RUNNING_POST_GAME
            self.menu_post_game = MenuPostGame(False)
        elif len(self.coin_group) == 0:
            self.is_running = RUNNING_POST_GAME
            self.menu_post_game = MenuPostGame(True)
        
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
        player = Player(50, GROUND_LEVEL, frame_rate_animation=50,frame_rate_movement=40, speed_run=10,scale=0.15)
        self.player = pg.sprite.GroupSingle(player)

        # Plataformas
        # Piedra
        self.platform_group = pg.sprite.Group()
        for i in range(11):
            x = 36 + 36 * i
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
        self.enemy_group = pg.sprite.Group()
        self.enemy_group.add(Enemy_Bug(500, GROUND_LEVEL, True, limit_left=400,limit_right=750, frame_rate_animation=400,frame_rate_movement=50, speed_walk=3,scale=2))
        self.enemy_group.add(Enemy_Alien(50, 200, True, frame_rate_animation=400,scale=2))

        # Monedas
        self.coin_group = pg.sprite.Group()
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
        
        self.timer = MarcadorTiempo(0,45,140,36,20)

    def nivel_2(self):
        # Marco
        self.marco = Marco().platform_group
        
        # Player
        player = Player(50, 384, frame_rate_animation=50,frame_rate_movement=40, speed_run=10,scale=0.15)
        self.player = pg.sprite.GroupSingle(player)

        # Plataformas
        # Piedra
        self.platform_group = pg.sprite.Group()
        for i in range(3):
            x = 36 + 36 * i
            self.platform_group.add(Platform(PISO_PIEDRA,x,384,is_platform=True,scale=2))
            self.platform_group.add(Platform(MURO_PIEDRA,x,420,scale=2))
            self.platform_group.add(Platform(MURO_PIEDRA,x,456,scale=2))
        
        for i in range(3):
            x = 656 + 36 * i
            self.platform_group.add(Platform(PISO_PIEDRA,x,384,is_platform=True,scale=2))
            self.platform_group.add(Platform(MURO_PIEDRA,x,420,scale=2))
            self.platform_group.add(Platform(MURO_PIEDRA,x,456,scale=2))
        
        # Nubes
        nubes = [{"largo" : 3, "x": 164, "y" : 384},
                {"largo" : 3, "x": 346, "y" : 384},
                {"largo" : 3, "x": 528, "y" : 384},
                {"largo" : 2, "x": 273, "y" : 250},
                {"largo" : 2, "x": 455, "y" : 250}]
        
        for nube in nubes:
            self.platform_group.add(Platform(NUBE_IZQUIERDA,nube["x"],nube["y"],transparent=True,is_platform=True,scale=2))
            for i in range(1, nube["largo"]):
                x = nube["x"] + 36 * i
                if i != nube["largo"] -1:
                    self.platform_group.add(Platform(NUBE_CENTRO,x,nube["y"],transparent=True,is_platform=True,scale=2))
                else:
                    self.platform_group.add(Platform(NUBE_DERECHA,x,nube["y"],transparent=True,is_platform=True,scale=2))
        
        # Enemigos
        self.enemy_group = pg.sprite.Group()
        self.enemy_group.add(Enemy_Block((ANCHO_VENTANA/8)*2+18, 100, 384, frame_rate_movement=50,scale=2))
        self.enemy_group.add(Enemy_Block((ANCHO_VENTANA/8)*4, 100, 384, frame_rate_movement=50,scale=2))
        self.enemy_group.add(Enemy_Block((ANCHO_VENTANA/8)*6-18, 100, 384, frame_rate_movement=50,scale=2))

        for i in range(14):
            x = 148 + 36 * i
            self.enemy_group.add(Enemy_Spikes(x,456,scale=2))    
        
        # Monedas
        self.coin_group = pg.sprite.Group()
        monedas = [{"largo": 1, "x" : 200, "y" : 320, "salteo" : False, "espacio" : 0},
                    {"largo": 1, "x" : 382, "y" : 320, "salteo" : False, "espacio" : 0},
                    {"largo": 1, "x" : 564, "y" : 320, "salteo" : False, "espacio" : 0},
                    {"largo": 1, "x" : 291, "y" : 186, "salteo" : False, "espacio" : 0},
                    {"largo": 1, "x" : 473, "y" : 186, "salteo" : False, "espacio" : 0},
                    {"largo": 1, "x" : 692, "y" : 320, "salteo" : False, "espacio" : 0}]
        
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
        
        self.timer = MarcadorTiempo(0,45,140,36,20)
    
    def nivel_3(self):
        # Marco
        self.marco = Marco().platform_group
        
        # Player
        player = Player(36, 164, frame_rate_animation=50,frame_rate_movement=40, speed_run=10,scale=0.15)
        self.player = pg.sprite.GroupSingle(player)

        # Plataformas
        # Piedra
        self.platform_group = pg.sprite.Group()
        for i in range(21):
            x = 36 + 36 * i
            self.platform_group.add(Platform(PISO_PIEDRA,x,36,scale=2))
        for i in range(16):
            x = 36 + 36 * i
            self.platform_group.add(Platform(MURO_PIEDRA,x,266,scale=2))
        for i in range(16):
            y = 70 + 30 * i
            self.platform_group.add(Platform(MURO_PIEDRA,728,y,scale=2))
        
        self.platform_group.add(Platform(PISO_PIEDRA,692,206,is_platform=True,scale=2))
        for i in range(9):
            y = 220 + 30 * i
            self.platform_group.add(Platform(MURO_PIEDRA,692,y,scale=2))

        self.platform_group.add(Platform(PISO_PIEDRA,36,206,is_platform=True,scale=2))
        self.platform_group.add(Platform(MURO_PIEDRA,36,236,scale=2))
        self.platform_group.add(Platform(PISO_PIEDRA,576,206,is_platform=True,scale=2))
        self.platform_group.add(Platform(MURO_PIEDRA,576,236,scale=2))

        # Nubes
        nubes = [{"largo" : 2, "x": 144, "y" : 200},
                {"largo" : 2, "x": 288, "y" : 200},
                {"largo" : 2, "x": 432, "y" : 200}]
        
        for nube in nubes:
            self.platform_group.add(Platform(NUBE_IZQUIERDA,nube["x"],nube["y"],transparent=True,is_platform=True,scale=2))
            for i in range(1, nube["largo"]):
                x = nube["x"] + 36 * i
                if i != nube["largo"] -1:
                    self.platform_group.add(Platform(NUBE_CENTRO,x,nube["y"],transparent=True,is_platform=True,scale=2))
                else:
                    self.platform_group.add(Platform(NUBE_DERECHA,x,nube["y"],transparent=True,is_platform=True,scale=2))

        # Enemigos
        self.enemy_group = pg.sprite.Group()
        for i in range(14):
            x = 72 + 36 * i
            self.enemy_group.add(Enemy_Spikes(x,236,scale=2)) 
        self.enemy_group.add(Enemy_Bug(300, GROUND_LEVEL, True, limit_left=100,limit_right=700, frame_rate_animation=400,frame_rate_movement=50, speed_walk=3,scale=2))
        self.enemy_group.add(Enemy_Bug(464, GROUND_LEVEL, False, limit_left=100,limit_right=700, frame_rate_animation=400,frame_rate_movement=50, speed_walk=3,scale=2))
        self.enemy_group.add(Enemy_Block(80*2, 300, GROUND_LEVEL, frame_rate_movement=50,scale=2))
        self.enemy_group.add(Enemy_Block(80*4, 300, GROUND_LEVEL, frame_rate_movement=50,scale=2))
        self.enemy_group.add(Enemy_Block(80*6, 300, GROUND_LEVEL, frame_rate_movement=50,scale=2))
        self.enemy_group.add(Enemy_Alien(680, 206, False, frame_rate_animation=400,scale=2))

        # Monedas
        self.coin_group = pg.sprite.Group()
        monedas = [{"largo": 7, "x" : 100, "y" : 130, "salteo" : True, "espacio" : 80},
                    {"largo": 1, "x" : 632, "y" : 240, "salteo" : False, "espacio" : 0},
                    {"largo": 1, "x" : 632, "y" : 350, "salteo" : False, "espacio" : 0},
                    {"largo": 1, "x" : 80*2-18, "y" : 370, "salteo" : False, "espacio" : 0},
                    {"largo": 1, "x" : 80*4-18, "y" : 370, "salteo" : False, "espacio" : 0},
                    {"largo": 1, "x" : 80*6-18, "y" : 370, "salteo" : False, "espacio" : 0}]
        
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

        self.timer = MarcadorTiempo(5,45,140,36,20)
    


        
        
