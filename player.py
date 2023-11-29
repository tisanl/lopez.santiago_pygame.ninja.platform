from auxiliar import SurfaceManager as sf
import pygame as pg
from constantes import *
from bullet import Bullet
from items import Heart

SPRITE_IDLE = "C:/Users/Usuario/Desktop/Proyecto Final/player_sprites/idle/Idle__00{0}.png"
SPRITE_RUN = "C:/Users/Usuario/Desktop/Proyecto Final/player_sprites/run/Run__00{0}.png"
SPRITE_JUMP = "C:/Users/Usuario/Desktop/Proyecto Final/player_sprites/jump/Jump__00{0}.png"
SPRITE_SHOOT = "C:/Users/Usuario/Desktop/Proyecto Final/player_sprites/jump_throw/Jump_Throw__00{0}.png"
SPRITE_JUMP_SHOOT = "C:/Users/Usuario/Desktop/Proyecto Final/player_sprites/jump_throw/Jump_Throw__00{0}.png"

SPRITE_BULLET = "C:/Users/Usuario/Desktop/Proyecto Final/player_sprites/Kunai.png"


class Player(pg.sprite.Sprite):
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  INIT DEL PLAYER  -------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def __init__(self, coord_x, coord_y, frame_rate_animation=100, frame_rate_movement=100, speed_run=10, gravity=10, jump=30, jump_max_high=150, scale=1):
        super().__init__()
    
        # Animaciones
        self.__iddle_r = sf.getSurfaceFromSeparateFiles(SPRITE_IDLE,0,9,flip=False,scale=scale)
        self.__iddle_l = sf.getSurfaceFromSeparateFiles(SPRITE_IDLE,0,9,flip=True,scale=scale)
        self.__run_r = sf.getSurfaceFromSeparateFiles(SPRITE_RUN,0,9,flip=False,scale=scale)
        self.__run_l = sf.getSurfaceFromSeparateFiles(SPRITE_RUN,0,9,flip=True,scale=scale)
        self.__jump_r = sf.getSurfaceFromSeparateFiles(SPRITE_JUMP,0,9,flip=False,scale=scale)
        self.__jump_l = sf.getSurfaceFromSeparateFiles(SPRITE_JUMP,0,9,flip=True,scale=scale)
        self.__shoot_r = sf.getSurfaceFromSeparateFiles(SPRITE_SHOOT,0,9,flip=False,scale=scale)
        self.__shoot_l = sf.getSurfaceFromSeparateFiles(SPRITE_SHOOT,0,9,flip=True,scale=scale)
        self.__jump_shoot_r = sf.getSurfaceFromSeparateFiles(SPRITE_JUMP_SHOOT,0,9,flip=False,scale=scale)
        self.__jump_shoot_l = sf.getSurfaceFromSeparateFiles(SPRITE_JUMP_SHOOT,0,9,flip=True,scale=scale)

        # Animacion dinamica
        self.__frame = 0                                            # Frame actual de la animacion que se esta reproduciendo. Se inicializa en 0
        self.__animacion_actual = self.__iddle_r                    # Se guarda la animacion que se esta reproduciendo. Se inicializa con Idle
        self.__image = self.__animacion_actual[self.__frame]        # Imagen actual que se esta reproducindo en la pantalla
        self.__frame_rate_animation = frame_rate_animation          # Variable que guarda la velocidad con la que se cambia la imagen
        self.__player_animation_time = 0                            # Variable que guarda el tiempo transcurrido desde que cambio la imagen

        # Posicion en pantalla
        self.__rect = self.image.get_rect(x=coord_x,y=coord_y)                                                  # Se obtiene el rectangulo de la imagen
        self.__player_foot = pg.Rect(self.rect.x +3, self.rect.y + self.rect.height + 1, self.rect.width-6, 3)  # Rectangulo de los pies del Jugador
        self.player_side_left = pg.Rect(self.rect.x -1 , self.rect.y, 1, self.rect.height)                      # Rectangulo del lado izquierdo del Jugador
        self.player_side_right = pg.Rect(self.rect.x + self.rect.width + 1, self.rect.y, 1, self.rect.height)   # Rectangulo del lado derecho del Jugador
        self.__frame_rate_movement = frame_rate_movement                                                        # Variable que guarda la velocidad con la que se ejecuta el movimiento

        # Variables de Movimiento
        self.__move_x = 0                   # La posicion en x del Jugador
        self.__move_y = 0                   # La posicion en y del Jugador
        self.__player_move_time = 0         # Variable que guarda el tiempo transcurrido desde que ejecuto un movimiento

        # Variables auxiliares
        self.__is_looking_right = True      # Bool que guarda la direccion donde mira el Jugador
        self.was_loogking_right = True      # Bool que guarda la direccion en la que miraba el Jugador
        self.__is_jumping = False           # Si esta saltando
        self.__is_jumping = False           # Si esta saltando
        self.__jump_limit = 0               # Limite del salto qeu se actualiza cuando el Jugador salta
        self.__is_falling = True            # Si esta cayendo
        self.__is_shooting = False          # Si esta disparando
        

        # Estadisticas
        self.__point = 0                        # Puntaje del Jugador en el nivel, se actualiza dinamicamente
        self.__speed_run = speed_run            # La velocidad del Jugador cuando corre
        self.__gravity = gravity                # La velocidad con la que el Jugador cae
        self.__jump = jump                      # La velocidad con la que el Jugador sube cuando salta
        self.__jump_max_high = jump_max_high    # La altura maxima que puede alcanzar el salto

        # Vida del Jugador
        self.lives_init = 3                     # Vida original del Jugador
        self.lives_actual = self.lives_init     # Vida actual del Jugador
        self.lives_group = pg.sprite.Group()    # Grupo que guardara los corazones

        # Bullet
        self.__bullet_speed = 7
        self.__bullet_scale = 0.3
        self.__shoot_time = 0
        self.__bullet_cooldown = 30

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # -----------------------------------------------------  MANEJO DE EVENTOS  ---------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def events(self,delta_ms,bullet_group,platform_group):
        keys = pg.key.get_pressed()

        # Run
        if keys[pg.K_RIGHT] and not keys[pg.K_LEFT] and not keys[pg.K_SPACE] and not self.__is_jumping and not self.__is_falling and not self.__is_shooting:
            self.run('Right')
        if keys[pg.K_LEFT] and not keys[pg.K_RIGHT] and not keys[pg.K_SPACE] and not self.__is_jumping and not self.__is_falling and not self.__is_shooting:
            self.run('Left')
        
        # Stay
        if not keys[pg.K_RIGHT] and not keys[pg.K_LEFT] and not keys[pg.K_SPACE] and not self.__is_jumping and not self.__is_falling and not self.__is_shooting:
            self.stay()
        
        # Jump
        if keys[pg.K_SPACE] and self.__is_falling == False:
            if self.__is_jumping == False:
                self.__jump_limit = self.rect.y - self.__jump_max_high
                self.__is_jumping = True
            if keys[pg.K_RIGHT]:
                self.jump("Right")
            elif keys[pg.K_LEFT]:
                self.jump("Left")
            else:
                self.jump("stay")
            if self.rect.y <= self.__jump_limit:
                self.__is_jumping = False
        else:
            self.__is_jumping = False

        # Fall 2.0
        if not self.is_on_plataform(platform_group) and not self.__is_jumping:
            self.__is_falling = True
            if keys[pg.K_RIGHT]:
                self.fall("Right")
            elif keys[pg.K_LEFT]:
                self.fall("Left")
            else:
                self.fall("stay")
        elif self.__is_falling:
            self.__is_falling = False
            self.__move_y = 0

        # Shoot
        if keys[pg.K_z] and not self.__is_shooting:
            self.shoot(delta_ms,bullet_group)
        elif self.__is_shooting and self.__frame == len(self.__shoot_r) - 1:
            self.__frame_rate_animation = 100
            self.__is_shooting = False
            
        
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
        if self.__animacion_actual != self.__jump_r and self.__animacion_actual != self.__jump_l and self.__animacion_actual != self.__jump_shoot_r and self.__animacion_actual != self.__jump_shoot_l:
            self.__frame = 0
        match direction:
            case 'Right':
                if self.__is_shooting:
                    self.__set_y_animations_preset(self.__speed_run, -self.__jump, self.__jump_shoot_r, True)
                else:
                    self.__set_y_animations_preset(self.__speed_run, -self.__jump, self.__jump_r, True)
            case 'Left':
                if self.__is_shooting:
                    self.__set_y_animations_preset(-self.__speed_run, -self.__jump, self.__jump_shoot_l, False)
                else:
                    self.__set_y_animations_preset(-self.__speed_run, -self.__jump, self.__jump_l, False)
            case "stay":
                if self.__is_looking_right:
                    if self.__is_shooting:
                        self.__set_y_animations_preset(0, -self.__jump, self.__jump_shoot_r, True)
                    else:
                        self.__set_y_animations_preset(0, -self.__jump, self.__jump_r, True)
                else:
                    if self.__is_shooting:
                        self.__set_y_animations_preset(0, -self.__jump, self.__jump_shoot_l, False)
                    else:
                        self.__set_y_animations_preset(0, -self.__jump, self.__jump_l, False)
    
    def fall(self, direction:str):
        if self.__animacion_actual != self.__jump_r and self.__animacion_actual != self.__jump_l and self.__animacion_actual != self.__jump_shoot_r and self.__animacion_actual != self.__jump_shoot_l:
            self.__frame = 0
        match direction:
            case 'Right':
                if self.__is_shooting:
                    self.__set_y_animations_preset(self.__speed_run,self.__gravity, self.__jump_shoot_r, True)
                else:
                    self.__set_y_animations_preset(self.__speed_run,self.__gravity, self.__jump_r, True)
            case 'Left':
                if self.__is_shooting:
                    self.__set_y_animations_preset(-self.__speed_run,self.__gravity, self.__jump_shoot_l, False)
                else:
                    self.__set_y_animations_preset(-self.__speed_run,self.__gravity, self.__jump_l, False)
            case "stay":
                if self.__is_looking_right:
                    if self.__is_shooting:
                        self.__set_y_animations_preset(0,self.__gravity, self.__jump_shoot_r, True)
                    else:
                        self.__set_y_animations_preset(0,self.__gravity, self.__jump_r, True)
                else:
                    if self.__is_shooting:
                        self.__set_y_animations_preset(0,self.__gravity, self.__jump_shoot_l, False)
                    else:
                        self.__set_y_animations_preset(0,self.__gravity, self.__jump_l, False)
    
    def shoot(self,delta_ms,bullet_group):
        self.__shoot_time += delta_ms
        if self.__shoot_time >= self.__bullet_cooldown:
            self.__frame_rate_animation = self.__bullet_cooldown
            self.__frame = 0
            if not self.__is_jumping or not self.__is_falling:
                if self.__is_looking_right:
                    self.__set_x_animations_preset(0, self.__shoot_r, True)
                else:
                    self.__set_x_animations_preset(0, self.__shoot_l, False)
            self.__is_shooting = True
            self.__shoot_time = 0
            bullet_group.add(Bullet(SPRITE_BULLET,self.__rect.x,self.__rect.centery,self.__bullet_speed,self.__is_looking_right,scale=self.__bullet_scale))

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------  FUNCIONES DE VIDA DEL JUGADOR  ------------------------------------------------------------------ #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ # 
    def update_lives(self):
        group = pg.sprite.Group()
        for i in range(self.lives_actual):
            x = 36 + i * 27
            group.add(Heart(x,36,scale=1.5))
        for i in range(self.lives_init - self.lives_actual):
            x = 36 + self.lives_actual * 27 + i * 27
            group.add(Heart(x,36,empty=True,scale=1.5))
        self.lives_group = group
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------  FUNCIONES DE POSICION EN PANTALLA  -------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ # 
    def is_on_plataform(self,platform_group):
        retorno = False
        if self.__player_foot.y >= GROUND_LEVEL:
            retorno = True
        else:
            for platform in platform_group:
                if platform.is_platform and self.__player_foot.colliderect(platform.rect_platform):
                    retorno = True
                    break
        return retorno     
        
    def __set_x_animations_preset(self, move_x, animation_list:list[pg.surface.Surface], look_r:bool):
        self.__move_x = move_x
        self.__animacion_actual = animation_list
        self.__is_looking_right = look_r
        
    def __set_y_animations_preset(self, move_x, move_y, animation_list:list[pg.surface.Surface], look_r:bool):
        self.__move_x = move_x
        self.__move_y = move_y
        self.__is_looking_right = look_r
        self.__animacion_actual = animation_list
    
    def __set_borders_limits(self, platform_group):
        pixels_move = 0
        esta_colicionando = False
        for platform in platform_group:
                if not platform.transparent and \
                (self.player_side_left.colliderect(platform.rect) or self.player_side_right.colliderect(platform.rect)):
                    esta_colicionando = True
                    break
        if self.__move_x > 0 and (not esta_colicionando or self.was_loogking_right != self.__is_looking_right):
            pixels_move = self.__move_x if self.player_side_right.x < 764 else 0
        elif self.__move_x < 0 and (not esta_colicionando or self.was_loogking_right != self.__is_looking_right):
            pixels_move = self.__move_x if self.player_side_left.x > 36 else 0
        self.was_loogking_right = self.__is_looking_right
        return pixels_move

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------  ACTUALIZACIONES DEL JUGADOR  -------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def do_movement(self, delta_ms,platform_group):
        self.__player_move_time += delta_ms
        if self.__player_move_time >= self.__frame_rate_movement:
            self.__player_move_time = 0
            self.rect.x += self.__set_borders_limits(platform_group)
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
    
    def update(self, delta_ms,bullet_group,platform_group):
        self.__player_foot = pg.Rect(self.rect.x + 3, self.rect.y + self.rect.height + 1, self.rect.width -6, 1)
        self.player_side_left = pg.Rect(self.rect.x + 3, self.rect.y + 10, 1, self.rect.height - 20)
        self.player_side_right = pg.Rect(self.rect.x + self.rect.width + 3, self.rect.y + 10, 1, self.rect.height - 20)
        self.events(delta_ms,bullet_group,platform_group)
        self.update_lives()
        self.do_movement(delta_ms,platform_group)
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
    
    @property
    def player_foot(self):
        return self.__player_foot
    @player_foot.setter
    def player_foot(self,player_foot):
        self.__player_foot = player_foot