from auxiliar import SurfaceManager as sf
import pygame as pg
from constantes import *
from bullet import Bullet

BUG_WALK = "C:/Users/Usuario/Desktop/Proyecto Final/enemy_sprites/bug_walk_0{0}.png"
BUG_DEATH = "C:/Users/Usuario/Desktop/Proyecto Final/enemy_sprites/bug_death_0{0}.png"


class Enemy_Bug(pg.sprite.Sprite):
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  INIT DEL PLAYER  -------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def __init__(self, coord_x, coord_y,limit_left,limit_right, frame_rate_animation=100, frame_rate_movement=100, speed_walk=10,scale=1):
        super().__init__()
    
        # Animaciones
        self.__speed_walk_r = sf.getSurfaceFromSeparateFiles(BUG_WALK,1,2,flip=False,scale=scale)
        self.__speed_walk_l = sf.getSurfaceFromSeparateFiles(BUG_WALK,1,2,flip=True,scale=scale)
        self.__death_r = sf.getSurfaceFromSeparateFiles(BUG_DEATH,1,2,flip=False,scale=scale)
        self.__death_l = sf.getSurfaceFromSeparateFiles(BUG_DEATH,1,2,flip=True,scale=scale)

        # Animacion dinamica
        self.__frame = 0                                            # Frame actual de la animacion que se esta reproduciendo. Se inicializa en 0
        self.__animacion_actual = self.__speed_walk_l               # Se guarda la animacion que se esta reproduciendo. Se inicializa con Idle
        self.__image = self.__animacion_actual[self.__frame]        # Imagen actual que se esta reproducindo en la pantalla
        self.__rect = self.image.get_rect()                         # Se obtiene el rectangulo de la imagen
        self.__rect.x = coord_x
        self.__rect.y = coord_y - self.rect.height
        self.__is_looking_right = True                              # Bool que guarda la direccion donde mira el Jugador
        self.__frame_rate_animation = frame_rate_animation          # Variable que guarda la velocidad con la que se cambia la imagen
        self.__enemy_animation_time = 0                             # Variable que guarda el tiempo transcurrido desde que cambio la imagen

        # Posicion en pantalla y dinamicas del movimiento
        self.__move_x = speed_walk                                  # La posicion en x del Jugador
        self.__speed_walk = speed_walk                              # La velocidad del Jugador cuando corre
        self.__enemy_move_time = 0                                  # Variable que guarda el tiempo transcurrido desde que ejecuto un movimiento
        self.__frame_rate_movement = frame_rate_movement            # Variable que guarda la velocidad con la que se ejecuta el movimiento

        self.__limit_left = limit_left
        self.__limit_right = limit_right

        # Estadisticas
        self.__lives = 3

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  FUNCIONES DE ACCIONES  -------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def patrullar(self):  # Ajusta al jugador a los limites de la pantalla
        if self.rect.x <= self.__limit_left:
            self.__set_x_animations_preset(self.__speed_walk, self.__speed_walk_l, True)
        if self.rect.x + self.rect.width >= self.__limit_right:
            self.__set_x_animations_preset(-self.__speed_walk, self.__speed_walk_r, False)
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------  FUNCIONES DE POSICION EN PANTALLA  -------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #     
    def __set_x_animations_preset(self, move_x, animation_list:list[pg.surface.Surface], look_r:bool):
        self.__move_x = move_x
        self.__animacion_actual = animation_list
        self.__is_looking_right = look_r
        
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------  ACTUALIZACIONES DEL JUGADOR  -------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #   
    def do_movement(self, delta_ms):
        self.__enemy_move_time += delta_ms
        if self.__enemy_move_time >= self.__frame_rate_movement:
            self.__enemy_move_time = 0
            self.__rect.x += self.__move_x
            #if self.__enemy_foot <= GROUND_LEVEL:
                #self.rect.y += 10

    def do_animation(self, delta_ms):
        self.__enemy_animation_time += delta_ms
        if self.__enemy_animation_time >= self.__frame_rate_animation:
            self.__enemy_animation_time = 0
            if self.__frame < len(self.__animacion_actual) - 1:
                self.__frame += 1
            else:
                self.__frame = 0
            self.image = self.__animacion_actual[self.__frame]
    
    def update(self, delta_ms, bullet_group,player):
        self.patrullar()
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # --------------------------------------------------  GETTERS Y SETTERS  ------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #   
    @property
    def image(self):
        return self.__image
    @image.setter
    def image(self,image):
        self.__image = image
    
    @property
    def rect(self):
        return self.__rect
    @rect.setter
    def rect(self,rect):
        self.__rect = rect
    
    @property
    def bullet_group(self):
        return self.__bullet_group
    @bullet_group.setter
    def bullet_group(self,bullet_group):
        self.__bullet_group = bullet_group