from auxiliar import SurfaceManager as sf
import pygame as pg
from constantes import *

SPRITE_IDLE = "C:/Users/Usuario/Desktop/Proyecto Final/Proyecto Final/player_sprites/idle/Idle__00{0}.png"
SPRITE_RUN = "C:/Users/Usuario/Desktop/Proyecto Final/Proyecto Final/player_sprites/run/Run__00{0}.png"
SPRITE_JUMP = "C:/Users/Usuario/Desktop/Proyecto Final/Proyecto Final/player_sprites/jump/Jump__00{0}.png"
SPRITE_FALL = "C:/Users/Usuario/Desktop/Proyecto Final/Proyecto Final/player_sprites/glide/Glide_00{0}.png"


class Player(pg.sprite.Sprite):
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  INIT DEL PLAYER  -------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def __init__(self, coord_x, coord_y, frame_rate_animation=100, frame_rate_movement=100, speed_run=10, gravity=5, jump=32, jump_max_high=400, scale=1):
        super().__init__()
    
        # Animaciones
        self.__iddle_r = sf.getSurfaceFromSeparateFiles(SPRITE_IDLE,0,9,flip=False,scale=scale)
        self.__iddle_l = sf.getSurfaceFromSeparateFiles(SPRITE_IDLE,0,9,flip=True,scale=scale)
        self.__run_r = sf.getSurfaceFromSeparateFiles(SPRITE_RUN,0,9,flip=False,scale=scale)
        self.__run_l = sf.getSurfaceFromSeparateFiles(SPRITE_RUN,0,9,flip=True,scale=scale)
        self.__jump_r = sf.getSurfaceFromSeparateFiles(SPRITE_JUMP,0,9,flip=False,scale=scale)
        self.__jump_l = sf.getSurfaceFromSeparateFiles(SPRITE_JUMP,0,9,flip=True,scale=scale)
        self.__fall_r = sf.getSurfaceFromSeparateFiles(SPRITE_FALL,0,9,flip=False,scale=scale)
        self.__fall_l = sf.getSurfaceFromSeparateFiles(SPRITE_FALL,0,9,flip=True,scale=scale)

        # Animacion dinamica
        self.__frame = 0                                            # Frame actual de la animacion que se esta reproduciendo. Se inicializa en 0
        self.__animacion_actual = self.__iddle_r                    # Se guarda la animacion que se esta reproduciendo. Se inicializa con Idle
        self.__image = self.__animacion_actual[self.__frame]        # Imagen actual que se esta reproducindo en la pantalla
        self.__rect = self.image.get_rect(x=coord_x,y=coord_y)      # Se obtiene el rectangulo de la imagen
        self.__is_looking_right = True                              # Bool que guarda la direccion donde mira el Jugador
        self.__frame_rate_animation = frame_rate_animation          # Variable que guarda la velocidad con la que se cambia la imagen
        self.__player_animation_time = 0                            # Variable que guarda el tiempo transcurrido desde que cambio la imagen

        # Posicion en pantalla y dinamicas del movimiento
        self.__move_x = coord_x                                     # La posicion en x del Jugador
        self.__move_y = coord_y                                     # La posicion en y del Jugador
        self.__speed_run = speed_run                                # La velocidad del Jugador cuando corre
        self.__player_move_time = 0                                 # Variable que guarda el tiempo transcurrido desde que ejecuto un movimiento
        self.__gravity = gravity                                    # La velocidad con la que el Jugador cae
        self.__jump = jump                                          # La velocidad con la que el Jugador sube cuando salta
        self.__jump_max_high = jump_max_high                        # La altura maxima que puede alcanzar el salto
        self.__jump_limit = 0
        self.__is_jumping = False                                   # Si esta saltando
        self.__is_falling = False                                   # Si esta cayendo
        self.__frame_rate_movement = frame_rate_movement            # Variable que guarda la velocidad con la que se ejecuta el movimiento
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # -----------------------------------------------------  MANEJO DE EVENTOS  ---------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def events(self):
        keys = pg.key.get_pressed()

        # Run
        if keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
            self.run('Right')
        if keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
            self.run('Left')
        
        # Stay
        if not keys[pg.K_RIGHT] and not keys[pg.K_LEFT] and not keys[pg.K_SPACE] and self.__is_falling == False:
            self.stay()
        
        # Jump
        if keys[pg.K_SPACE] and self.__is_falling == False:
            if self.__is_jumping == False:
                self.__jump_limit = self.rect.y - self.__jump_max_high
                self.__is_jumping = True
            if keys[pg.K_RIGHT] or self.__is_looking_right:
                self.jump("Right")
            elif keys[pg.K_LEFT] or self.__is_looking_right == False:
                self.jump("Left")

        if (not keys[pg.K_SPACE] or (self.rect.y <= self.__jump_limit)) and self.__is_jumping == True:
            self.__is_jumping = False
            self.__is_falling = True
            print("helouda")

        # Fall
        if self.rect.y <= GROUND_LEVEL and self.__is_jumping == False:
            self.__is_falling = True
            if keys[pg.K_RIGHT] or self.__is_looking_right:
                self.fall("Right")
            elif keys[pg.K_LEFT] or self.__is_looking_right == False:
                self.fall("Left")
        elif self.rect.y >= GROUND_LEVEL - 100 and self.__is_falling == True:
            self.__is_falling = False
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  FUNCIONES DE ACCIONES  -------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def run(self, direction: str = 'Right'):
        if self.__animacion_actual != self.__run_r and self.__animacion_actual != self.__run_l:
            self.__frame = 0
        match direction:
            case 'Right':
                self.__set_x_animations_preset(self.__speed_run, self.__run_r, True)
            case 'Left':
                self.__set_x_animations_preset(-self.__speed_run, self.__run_l, False)
    
    def stay(self):
        if self.__animacion_actual != self.__iddle_l and self.__animacion_actual != self.__iddle_r:
            self.__animacion_actual = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__frame = 0
            self.__move_x = 0
            self.__move_y = 0
    
    def jump(self, direction:str):
        if self.__animacion_actual != self.__jump_r and self.__animacion_actual != self.__jump_l:
            self.__frame = 0
        match direction:
            case 'Right':
                self.__set_y_animations_preset(self.__speed_run, -self.__jump, self.__jump_r, True)
            case 'Left':
                self.__set_y_animations_preset(-self.__speed_run, -self.__jump, self.__jump_l, False)
    
    def fall(self, direction:str):
        if self.__animacion_actual != self.__fall_r and self.__animacion_actual != self.__fall_l:
            self.__frame = 0
        match direction:
            case 'Right':
                self.__set_y_animations_preset(self.__speed_run, self.__gravity, self.__fall_r, True)
            case 'Left':
                self.__set_y_animations_preset(-self.__speed_run, self.__gravity, self.__fall_l, False)

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------  FUNCIONES DE POSICION EN PANTALLA  -------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #     
    def __set_x_animations_preset(self, move_x, animation_list:list[pg.surface.Surface], look_r:bool):
        self.__move_x = move_x
        self.__animacion_actual = animation_list
        self.__is_looking_right = look_r
        
    def __set_y_animations_preset(self, move_x, move_y, animation_list:list[pg.surface.Surface], look_r:bool):
        self.__move_x = move_x
        self.__move_y = move_y
        self.__is_looking_right = look_r
        self.__animacion_actual = animation_list
    
    def __set_borders_limits(self):
        pixels_move = 0
        if self.__move_x > 0:
            pixels_move = self.__move_x if self.rect.x < ANCHO_VENTANA - self.image.get_width() else 0
        elif self.__move_x < 0:
            pixels_move = self.__move_x if self.rect.x > 0 else 0
        return pixels_move
    
    def __set_ground_level(self):
        pixels_move = 0
        if self.__move_y > 0:
            pixels_move = self.__move_y if self.rect.y < GROUND_LEVEL else 0
        else:
            pixels_move = 0
            self.__is_falling = False
        return pixels_move

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------  ACTUALIZACIONES DEL JUGADOR  -------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #   
    def do_movement(self, delta_ms):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate_movement:
            self.__player_move_time = 0
            self.rect.x += self.__set_borders_limits()
            self.rect.y += self.__move_y

    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms
        if self.__player_animation_time >= self.__frame_rate_animation:
            self.__player_animation_time = 0
            if self.__frame < len(self.__animacion_actual) - 1:
                self.__frame += 1
            else:
                self.__frame = 0
            self.image = self.__animacion_actual[self.__frame]

                # if self.__is_jumping:
                #     self.__is_jumping = False
                #     self.__move_y = 0
    
    def update(self, delta_ms):
        self.events()
        self.do_movement(delta_ms)
        self.do_animation(delta_ms)
    

        #if DEBUG:
            #pg.draw.rect(screen, 'red', self.rect)
            #pg.draw.rect(screen, 'green', self.rect.bottom)
    
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