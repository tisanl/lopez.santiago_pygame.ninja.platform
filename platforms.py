import pygame as pg
from constantes import *
from auxiliar import SurfaceManager as sf

GRASS_PLATFORM = "platform_sprites/platform_grass.png"
GROUND = "platform_sprites/ground.png"
BLACK_SPRITE = "platform_sprites/black.png"
MARCO_ARRIBA = "platform_sprites/marco_arriba.png"
MARCO_ABAJO = "platform_sprites/marco_abajo.png"
MARCO_DERECHA = "platform_sprites/marco_der.png"
MARCO_IZQUIERDA = "platform_sprites/marco_izq.png"
MARCO_HORIZONTAL = "platform_sprites/marco_horizontal.png"
MARCO_VERTICAL = "platform_sprites/marco_vertical.png"
MARCO_ESQUINA = "platform_sprites/marco_esquina.png"

class Marco:
    def __init__(self):
        self.platform_group = pg.sprite.Group()
        
        # Marco Inferior Tierra
        for i in range(1,ANCHO_VENTANA // 36):
            x = 0 + 36 * i
            self.platform_group.add(Platform(GRASS_PLATFORM,x,492,scale=2))
        
        # Marco Inferior Tierra
        for i in range(1,ANCHO_VENTANA // 36):
            x = 0 + 36 * i
            self.platform_group.add(Platform(GROUND,x,528,scale=2))

        # Esquinas
        self.platform_group.add(Platform(MARCO_ESQUINA,0,0,scale=2))
        self.platform_group.add(Platform(MARCO_ESQUINA,0,564,scale=2))
        self.platform_group.add(Platform(MARCO_ESQUINA,764,0,scale=2))
        self.platform_group.add(Platform(MARCO_ESQUINA,764,564,scale=2))

        # Marco Superior
        for i in range(2,ANCHO_VENTANA // 36 - 1):
            x = 0 + 36 * i
            self.platform_group.add(Platform(MARCO_HORIZONTAL,x,0,scale=2))
        self.platform_group.add(Platform(MARCO_IZQUIERDA,36,0,scale=2))
        self.platform_group.add(Platform(MARCO_DERECHA,728,0,scale=2))
        
        # Marco Inferior
        for i in range(2,ANCHO_VENTANA // 36 - 1):
            x = 0 + 36 * i
            self.platform_group.add(Platform(MARCO_HORIZONTAL,x,564,scale=2))
        self.platform_group.add(Platform(MARCO_IZQUIERDA,36,564,scale=2))
        self.platform_group.add(Platform(MARCO_DERECHA,728,564,scale=2))

        # Marco Izquierdo
        for i in range(2,ALTO_VENTANA // 36 - 1):
            y = 0 + 36 * i
            self.platform_group.add(Platform(MARCO_VERTICAL,0,y,scale=2))
        self.platform_group.add(Platform(MARCO_ARRIBA,0,36,scale=2))
        self.platform_group.add(Platform(MARCO_ABAJO,0,528,scale=2))

        # Marco Derecho
        for i in range(2,ALTO_VENTANA // 36 - 1):
            y = 0 + 36 * i
            self.platform_group.add(Platform(MARCO_VERTICAL,764,y,scale=2))
        self.platform_group.add(Platform(MARCO_ARRIBA,764,36,scale=2))
        self.platform_group.add(Platform(MARCO_ABAJO,764,528,scale=2))

class Platform(pg.sprite.Sprite):
    def __init__(self,sprite_route,pos_x,pos_y,transparent=False,is_platform=False,scale=1):
        super().__init__()
        self.image = sf.getSurfaceFromFile(sprite_route,flip=False,scale=scale)
        self.rect = self.image.get_rect(x=pos_x, y=pos_y)
        self.transparent = transparent
        self.is_platform = is_platform
        self.rect_platform = pg.Rect(self.rect.x,self.rect.y, self.rect.width, 10)

'''
        for i in range(ANCHO_VENTANA // 36 + 1):
            x = 0 + 36 * i
            self.platform_group.add(Platform(BLACK_SPRITE,x,564,scale=2))
        for i in range(ANCHO_VENTANA // 36 + 1):
            x = 0 + 36 * i
            self.platform_group.add(Platform(BLACK_SPRITE,x,0,scale=2))
        for i in range(ALTO_VENTANA // 36 + 1):
            y = 0 + 36 * i
            self.platform_group.add(Platform(BLACK_SPRITE,0,y,scale=2))
        for i in range(ALTO_VENTANA // 36 + 1):
            y = 0 + 36 * i
            self.platform_group.add(Platform(BLACK_SPRITE,764,y,scale=2))

'''