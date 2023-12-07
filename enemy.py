from auxiliar import SurfaceManager as sf
import pygame as pg
from constantes import *
from bullet import Bullet

BUG_WALK = "enemy_sprites/bug_walk_0{0}.png"
BUG_DEATH = "enemy_sprites/bug_death_0{0}.png"

ALIEN_IDLE = "enemy_sprites/alien_idle_0{0}.png"
ALIEN_DEATH = "enemy_sprites/alien_death_0{0}.png"
LASER = "enemy_sprites/laser.png"

BLOCK_STAY = "enemy_sprites/block_stay.png"
BLOCK_ATTACKING = "enemy_sprites/block_falling.png"

SPIKES = "enemy_sprites/spikes.png"

TUBERIA = "enemy_sprites/tuberia.png"

class Enemy_Bug(pg.sprite.Sprite):
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  INIT DEL PLAYER  -------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def __init__(self, coord_x, coord_y,is_looking_right,limit_left,limit_right, frame_rate_animation=100, frame_rate_movement=100, speed_walk=10,scale=1):
        super().__init__()
        # Variables generales
        self.is_shooter = False
        self.insta_kill = False
        self.is_death = False
        
        # Vida del Enemigo
        self.__lives = 3        
        
        # Limites de movimiento en x
        self.__limit_left = limit_left
        self.__limit_right = limit_right

        # Variable auxiliar
        self.__is_looking_right = is_looking_right
        
        # Tiempo para hacer que el enemigo no reciba daño por un ratito si le acaba de pasar
        self.__damage_frame_time = 300
        self.__enemy_damage_time = 0
        self.__death_frame_time = 3500

        # Animaciones
        self.__speed_walk_r = sf.getSurfaceFromSeparateFiles(BUG_WALK,1,2,flip=True,scale=scale)
        self.__speed_walk_l = sf.getSurfaceFromSeparateFiles(BUG_WALK,1,2,flip=False,scale=scale)
        self.__death_r = sf.getSurfaceFromSeparateFiles(BUG_DEATH,1,2,flip=True,scale=scale)
        self.__death_l = sf.getSurfaceFromSeparateFiles(BUG_DEATH,1,2,flip=False,scale=scale)
        
        # Animacion dinamica
        self.__frame = 0                                            # Frame actual de la animacion que se esta reproduciendo. Se inicializa en 0
        self.__animacion_actual = self.__speed_walk_r if self.__is_looking_right else self.__speed_walk_l    # Se guarda la animacion que se esta reproduciendo. Se inicializa con Idle
        self.__image = self.__animacion_actual[self.__frame]        # Imagen actual que se esta reproducindo en la pantalla
        self.__rect = self.image.get_rect()                         # Se obtiene el rectangulo de la imagen
        self.__rect.x = coord_x
        self.__rect.y = coord_y - self.rect.height
        self.__frame_rate_animation = frame_rate_animation          # Variable que guarda la velocidad con la que se cambia la imagen
        self.__enemy_animation_time = 0                             # Variable que guarda el tiempo transcurrido desde que cambio la imagen

        # Posicion en pantalla y dinamicas del movimiento
        self.__move_x = speed_walk if self.__is_looking_right else -speed_walk        # La posicion en x del Enemigo
        self.__speed_walk = speed_walk                              # La velocidad del Enemigo cuando corre
        self.__enemy_move_time = 0                                  # Variable que guarda el tiempo transcurrido desde que ejecuto un movimiento
        self.__frame_rate_movement = frame_rate_movement            # Variable que guarda la velocidad con la que se ejecuta el movimiento
        
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  FUNCIONES DE ACCIONES  -------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def patrullar(self):  # Ajusta al Enemigo a los limites de la pantalla
        if self.rect.x <= self.__limit_left:
            self.__set_x_animations_preset(self.__speed_walk, self.__speed_walk_r, True)
        if self.rect.x + self.rect.width >= self.__limit_right:
            self.__set_x_animations_preset(-self.__speed_walk, self.__speed_walk_l, False)
    
    def player_collitions(self, delta_ms, player):
        self.__enemy_damage_time += delta_ms
        if pg.sprite.spritecollide(self, player.sprite.bullet_group, True) and self.__enemy_damage_time >= self.__damage_frame_time and not self.is_death:
            self.__enemy_damage_time = 0
            self.__lives -= 1
    
    def death(self, delta_ms):
        if self.__lives <= 0: 
            if not self.is_death:
                self.is_death = True
                self.__move_x = 0
                self.__frame = 0

                if self.__is_looking_right:
                    self.__animacion_actual = self.__death_r
                else:
                    self.__animacion_actual = self.__death_l
            else:
                self.__enemy_damage_time += delta_ms
                if self.__enemy_damage_time >= self.__death_frame_time:
                    self.kill()
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------  FUNCIONES DE POSICION EN PANTALLA  -------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #     
    def __set_x_animations_preset(self, move_x, animation_list:list[pg.surface.Surface], look_r:bool):
        self.__move_x = move_x
        self.__animacion_actual = animation_list
        self.__is_looking_right = look_r
        
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------  ACTUALIZACIONES DEL ENEMIGO  -------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def do_movement(self, delta_ms):
        self.__enemy_move_time += delta_ms
        if self.__enemy_move_time >= self.__frame_rate_movement:
            self.__enemy_move_time = 0
            self.__rect.x += self.__move_x

    def do_animation(self, delta_ms):
        self.__enemy_animation_time += delta_ms
        if self.__enemy_animation_time >= self.__frame_rate_animation:
            self.__enemy_animation_time = 0
            if self.__frame < len(self.__animacion_actual) - 1:
                self.__frame += 1
            else:
                self.__frame = 0
            self.image = self.__animacion_actual[self.__frame]

    def update(self, delta_ms, player):
        self.patrullar()
        self.player_collitions(delta_ms, player)
        self.death(delta_ms)
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
    
class Enemy_Alien(pg.sprite.Sprite):
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  INIT DEL PLAYER  -------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def __init__(self, coord_x, coord_y, is_looking_right, frame_rate_animation=100,scale=1):
        super().__init__()
        # Variables generales
        self.is_shooter = True
        self.insta_kill = False
        self.is_death = False

        # Vida del Enemigo
        self.__lives = 3   

        # Cosas de balas
        self.bullet_group = pg.sprite.Group()
        self.__bullet_speed = 3
        self.__bullet_scale = 0.5
        self.__shoot_time = 0
        self.__bullet_cooldown = 2000
        
        # Variable auxiliar
        self.__is_looking_right = is_looking_right

        # Tiempo para hacer que el enemigo no reciba daño por un ratito si le acaba de pasar
        self.__damage_frame_time = 300
        self.__enemy_damage_time = 0
        self.__death_frame_time = 3500

        # Animaciones
        if self.__is_looking_right:
            self.__stay = sf.getSurfaceFromSeparateFiles(ALIEN_IDLE,1,2,flip=True,scale=scale)
            self.__death = sf.getSurfaceFromSeparateFiles(ALIEN_DEATH,1,2,flip=True,scale=scale)
            
        else:
            self.__stay = sf.getSurfaceFromSeparateFiles(ALIEN_IDLE,1,2,flip=False,scale=scale)
            self.__death = sf.getSurfaceFromSeparateFiles(ALIEN_DEATH,1,2,flip=False,scale=scale)
        
        # Animacion dinamica
        self.__frame = 0                                            # Frame actual de la animacion que se esta reproduciendo. Se inicializa en 0
        self.__animacion_actual = self.__stay                       # Se guarda la animacion que se esta reproduciendo. Se inicializa con Idle
        self.__image = self.__animacion_actual[self.__frame]        # Imagen actual que se esta reproducindo en la pantalla
        self.__frame_rate_animation = frame_rate_animation          # Variable que guarda la velocidad con la que se cambia la imagen
        self.__enemy_animation_time = 0                             # Variable que guarda el tiempo transcurrido desde que cambio la imagen
        
        # Rectangulos
        self.__rect = self.image.get_rect()                         # Se obtiene el rectangulo de la imagen
        self.__rect.x = coord_x
        self.__rect.y = coord_y - self.rect.height

        if self.__is_looking_right:
            self.shooting_colition_rect = pg.Rect(self.rect.x, self.rect.y - self.rect.height / 2, ANCHO_VENTANA - self.rect.x, self.rect.height * 1.5)
        else:
            self.shooting_colition_rect = pg.Rect(36, self.rect.y - self.rect.height / 2, ANCHO_VENTANA - 36*2, self.rect.height * 1.5)
        # Rectangulo al que si el Jugador coliciona se pone a disparar

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  FUNCIONES DE ACCIONES  -------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def shoot(self,delta_ms):
        self.__shoot_time += delta_ms
        if self.__shoot_time >= self.__bullet_cooldown:
            self.__shoot_time = 0
            self.bullet_group.add(Bullet(LASER,self.__rect.x + self.__rect.width / 2 ,self.__rect.centery,self.__bullet_speed,self.__is_looking_right,scale=self.__bullet_scale))
    
    def player_collitions(self, delta_ms, player):
        self.__enemy_damage_time += delta_ms
        if pg.sprite.spritecollide(self, player.sprite.bullet_group, True) and self.__enemy_damage_time >= self.__damage_frame_time and not self.is_death:
            self.__enemy_damage_time = 0
            self.__lives -= 1
    
    def death(self, delta_ms):
        if self.__lives <= 0: 
            if not self.is_death:
                self.is_death = True
                self.__frame = 0
                self.__animacion_actual = self.__death
            else:
                self.__enemy_damage_time += delta_ms
                if self.__enemy_damage_time >= self.__death_frame_time:
                    self.kill()

    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------  ACTUALIZACIONES DEL ENEMIGO  -------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def do_animation(self, delta_ms):
        self.__enemy_animation_time += delta_ms
        if self.__enemy_animation_time >= self.__frame_rate_animation:
            self.__enemy_animation_time = 0
            if self.__frame < len(self.__animacion_actual) - 1:
                self.__frame += 1
            else:
                self.__frame = 0
            self.image = self.__animacion_actual[self.__frame]

    def update(self, delta_ms,player):
        if self.shooting_colition_rect.colliderect(player.sprite.rect) and not self.is_death:
            self.shoot(delta_ms)
        self.player_collitions(delta_ms, player)
        self.death(delta_ms)
        self.bullet_group.update()
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
    
class Enemy_Block(pg.sprite.Sprite):
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  INIT DEL PLAYER  -------------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def __init__(self, coord_x, coord_y, fall_top,gravity=20, frame_rate_movement=100,scale=1):
        super().__init__()
        # Variables generales
        self.is_shooter = False
        self.insta_kill = False
        self.is_death = False

        # Variable auxiliar
        self.__is_getting_back = False

        # Animaciones
        self.__stay = sf.getSurfaceFromFile(BLOCK_STAY,flip=False,scale=scale)
        self.__attacking = sf.getSurfaceFromFile(BLOCK_ATTACKING,flip=False,scale=scale)
        self.__gravity = gravity
        self.__fall_top = fall_top
        self.__up_top = coord_y - 5
        
        # Animacion dinamica
        self.__image = self.__stay                                  # Imagen actual que se esta reproducindo en la pantalla

        self.__rect = self.image.get_rect()                         # Se obtiene el rectangulo de la imagen
        self.__rect.centerx = coord_x
        self.__rect.y = coord_y

        # Posicion en pantalla y dinamicas del movimiento
        self.__move_y = 0
        self.__enemy_move_time = 0                                  # Variable que guarda el tiempo transcurrido desde que ejecuto un movimiento
        self.__frame_rate_movement = frame_rate_movement            # Variable que guarda la velocidad con la que se ejecuta el movimiento

        self.attacking_colition_rect = pg.Rect(self.rect.x-15, self.rect.y + self.rect.height, self.rect.width + 30, self.__fall_top - self.rect.y)
        
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------------  FUNCIONES DE ACCIONES  -------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def attack(self,player):
        if self.rect.y + self.rect.height >= self.__fall_top:
            self.__image = self.__stay
            self.__is_getting_back = True
            self.__move_y = - 3
            print("Entro a volver")
        elif self.rect.y <= self.__up_top:
            print("Entro a bajar")
            self.__is_getting_back = False
            self.__move_y = 0
            self.rect.y = self.__up_top + 5
        elif self.attacking_colition_rect.colliderect(player.sprite.rect) and not self.__is_getting_back:
            print("Entro a atacar")
            self.__image = self.__attacking
            self.__move_y = self.__gravity
        
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    # ---------------------------------------------  ACTUALIZACIONES DEL ENEMIGO  -------------------------------------------------------------------- #
    # ------------------------------------------------------------------------------------------------------------------------------------------------ #
    def do_movement(self, delta_ms):
        self.__enemy_move_time += delta_ms
        if self.__enemy_move_time >= self.__frame_rate_movement:
            self.__enemy_move_time = 0
            self.__rect.y += self.__move_y

    def update(self, delta_ms, player):
        self.attack(player)
        self.do_movement(delta_ms)
    
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

class Enemy_Spikes(pg.sprite.Sprite):
    def __init__(self,pos_x,pos_y,scale=1):
        super().__init__()
        # Variables generales
        self.is_shooter = False
        self.insta_kill = True
        self.is_death = False

        # Imagen y posicion
        self.image = sf.getSurfaceFromFile(SPIKES,flip=False,scale=scale)
        self.rect = self.image.get_rect(x=pos_x, y=pos_y)

class EnemyBugSpawner(pg.sprite.Sprite):
    def __init__(self,pos_x,pos_y,bug,frame_spawn_time,scale=1):
        super().__init__()
        # Imagen y posicion
        self.image = sf.getSurfaceFromFile(TUBERIA,flip=False,scale=scale)
        self.rect = self.image.get_rect(x=pos_x, y=pos_y)

        # Bug
        self.__bug = bug

        # Cooldawn
        self.__spawn_time = frame_spawn_time
        self.__frame_spawn_time = frame_spawn_time
    
    def update(self, delta_ms,enemy_group):
        self.__spawn_time += delta_ms
        if self.__spawn_time >= self.__frame_spawn_time:
            self.__spawn_time = 0
            enemy_group.add(Enemy_Bug(self.__bug["pos_x"],
                                        self.__bug["pos_y"],
                                        self.__bug["is_looking_right"],
                                        self.__bug["limit_left"],
                                        self.__bug["limit_right"],
                                        self.__bug["frame_rate_animation"],
                                        self.__bug["frame_rate_movement"],
                                        self.__bug["speed_walk"],
                                        self.__bug["scale"]))