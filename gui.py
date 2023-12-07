import pygame as pg
from constantes import *
from auxiliar import SurfaceManager as sf
import sys
from auxiliar import FilesManager as fl

# CURSOR
CURSOR = "gui_sprites/cursor.png"

# FONDO MENU PRINCIPAL Y SELECCION DE NIVEL
FONDO_MENU_PRINCIPAL = "background/game_background_1.png"

# FONDO BLANCO
FONDO_BLANCO = "gui_sprites/back.png"
FONDO_AMARILLO = "gui_sprites/back_amarillo.png"

# BOTONES DE COLORES
BOTON_LIMPIO = "gui_sprites/botones/boton_limpio.png"
BOTON_LIMPIO_CUADRADO = "gui_sprites/botones/boton_limpio_cuadrado.png"
BOTON_LIMPIO_CHIQUITO = "gui_sprites/botones/boton_limpio_chiquito.png"
BOTON_AZUL = "gui_sprites/botones/boton_azul.png"
BOTON_ROJO = "gui_sprites/botones/boton_rojo.png"
BOTON_VERDE = "gui_sprites/botones/boton_verde.png"
BOTON_AMARILLO = "gui_sprites/botones/boton_amarillo.png"

# SONIDO
SOUND_UP = "gui_sprites/sonido/sound_up.png"
SOUND_DOWN = "gui_sprites/sonido/sound_down.png"
SOUND_OFF = "gui_sprites/sonido/sound_off.png"
SOUND_ON = "gui_sprites/sonido/sound_on.png"


class Cursor(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = sf.getSurfaceFromFile(CURSOR)
        self.rect = self.image.get_rect()  # Obtiene el rectángulo que rodea la imagen

    def update(self):
        # Actualiza la posición de la mira para seguir el cursor del mouse
        self.rect.center = pg.mouse.get_pos()

class Button(pg.sprite.Sprite):
    def __init__(self, sprite_rute,pos_x,pos_y,scale=1):
        super().__init__()
        self.image = sf.getSurfaceFromFile(sprite_rute,flip=False,scale=scale)
        self.rect = self.image.get_rect(x=pos_x, y=pos_y)

class BotonConTexto(pg.sprite.Sprite):
    def __init__(self, sprite_rute,pos_x, pos_y, texto, size_text, scale=1):
        super().__init__()
        self.sprite_rute = sprite_rute
        self.scale = scale
        self.image = sf.getSurfaceFromFile(self.sprite_rute,flip=False,scale=self.scale)
        self.rect = self.image.get_rect(x=pos_x, y=pos_y)

        self.__font = pg.font.Font(FONT, size_text)
        self.__text = self.__font.render(texto, True, "black")

        self.x_del_texto = (self.rect.width - self.__text.get_width()) / 2
        self.y_del_texto = (self.rect.height - self.__text.get_height()) / 2

        self.image.blit(self.__text,(self.x_del_texto,self.y_del_texto))

    def update_text(self, texto):
        self.image = sf.getSurfaceFromFile(self.sprite_rute,flip=False,scale=self.scale)
        self.__text = self.__font.render(texto, True, "black")
        self.image.blit(self.__text,(self.x_del_texto,self.y_del_texto))

class ButtonSwitch(pg.sprite.Sprite):
    def __init__(self, sprite_rute_1,sprite_rute_2,pos_x,pos_y,scale=1):
        super().__init__()
        self.image_1 = sf.getSurfaceFromFile(sprite_rute_1,flip=False,scale=scale)
        self.image_2 = sf.getSurfaceFromFile(sprite_rute_2,flip=False,scale=scale)
        self.image = self.image_1
        self.rect = self.image.get_rect(x=pos_x, y=pos_y)

        self.imagen_posterior = False
    
    def switch(self):
        if self.imagen_posterior:
            self.image = self.image_1
            self.imagen_posterior = False
        else:
            self.image = self.image_2
            self.imagen_posterior = True

class ButtonSwitchText(pg.sprite.Sprite):
    def __init__(self, sprite_rute_1,sprite_rute_2,pos_x,pos_y,texto,size_text,scale=1):
        super().__init__()
        self.image_1 = sf.getSurfaceFromFile(sprite_rute_1,flip=False,scale=scale)
        self.image_2 = sf.getSurfaceFromFile(sprite_rute_2,flip=False,scale=scale)
        self.image = self.image_1
        self.rect = self.image.get_rect(x=pos_x, y=pos_y)

        self.rect = self.image.get_rect(x=pos_x, y=pos_y)

        self.__font = pg.font.Font(FONT, size_text)
        self.__text = self.__font.render(texto, True, "black")

        self.x_del_texto = (self.rect.width - self.__text.get_width()) / 2
        self.y_del_texto = (self.rect.height - self.__text.get_height()) / 2

        self.image.blit(self.__text,(self.x_del_texto,self.y_del_texto))

        self.imagen_posterior = False
    
    def switch(self):
        if self.imagen_posterior:
            self.image = self.image_1
            self.imagen_posterior = False
        else:
            self.image = self.image_2
            self.imagen_posterior = True
        self.image.blit(self.__text,(self.x_del_texto,self.y_del_texto))

class MenuPrincipal:
    def __init__(self):
        #Fondo
        self.fondo = pg.transform.scale(pg.image.load(FONDO_MENU_PRINCIPAL), (ANCHO_VENTANA, ALTO_VENTANA))

        # Botones
        self.button_group = pg.sprite.Group()

        self.titulo = BotonConTexto(BOTON_LIMPIO,75,20,"MENU PRINCIPAL",55,scale=3.5)
        self.seleccion_nivel = BotonConTexto(BOTON_AZUL,210,200,"SELECCION DE NIVEL",25,scale=2)
        self.puntuaciones = BotonConTexto(BOTON_VERDE,210,295,"PUNTUACIONES",25,scale=2)
        self.sonido = BotonConTexto(BOTON_AMARILLO,210,390,"SONIDO",25,scale=2)
        self.salir = BotonConTexto(BOTON_ROJO,210,485,"SALIR",25,scale=2)
        self.button_group.add(self.titulo)
        self.button_group.add(self.seleccion_nivel)
        self.button_group.add(self.puntuaciones)
        self.button_group.add(self.sonido)
        self.button_group.add(self.salir)
    
    def update(self, eventos, game):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                lista_botones = pg.sprite.spritecollide(game.cursor.sprite, self.button_group, False)
                for boton in lista_botones:
                    if boton == self.seleccion_nivel:
                        game.is_running = MENU_SELECCION
                    elif boton == self.sonido:
                        game.is_running = CONFIGURACION_SONIDO
                        game.was_running = MENU_PRINCIPAL
                    elif boton == self.puntuaciones:
                        game.is_running = MENU_PUNTUACIONES
                    elif boton == self.salir:
                        pg.quit() 
                        sys.exit()

class MenuSeleccionNivel:
    def __init__(self):
        #Fondo
        self.fondo = pg.transform.scale(pg.image.load(FONDO_MENU_PRINCIPAL), (ANCHO_VENTANA, ALTO_VENTANA))

        # Botones
        self.button_group = pg.sprite.Group()
        self.titulo = BotonConTexto(BOTON_LIMPIO,75,30,"SELECCION DE NIVEL",45,scale=3.5)
        self.nivel_1 = BotonConTexto(BOTON_AZUL,210,230,"NIVEL 1",25,scale=2)
        self.nivel_2 = BotonConTexto(BOTON_AZUL,210,330,"NIVEL 2",25,scale=2)
        self.nivel_3 = BotonConTexto(BOTON_AZUL,210,430,"NIVEL 3",25,scale=2)
        self.volver = BotonConTexto(BOTON_ROJO,20,500,"SALIR",20,scale=0.7)
        self.button_group.add(self.titulo)
        self.button_group.add(self.nivel_1)
        self.button_group.add(self.nivel_2)
        self.button_group.add(self.nivel_3)
        self.button_group.add(self.volver)
    
    def update(self, eventos, game):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                lista_botones = pg.sprite.spritecollide(game.cursor.sprite, self.button_group, False)
                for boton in lista_botones:
                    if boton == self.nivel_1:
                        game.level_selected = 1
                        game.nivel_1()
                    elif boton == self.nivel_2:
                        game.level_selected = 2
                        game.nivel_2()
                    elif boton == self.nivel_3:
                        game.level_selected = 3
                        game.nivel_3()
                    elif boton == self.volver:
                        game.is_running = MENU_PRINCIPAL
                        game.enter_menu = 0

class MenuPostGame:
    def __init__(self,win:bool):
        #Fondo
        
        self.fondo = pg.transform.scale(pg.image.load(FONDO_BLANCO), ((ANCHO_VENTANA/6)*4.5, (ALTO_VENTANA/6)*4.5))
        x = ((ANCHO_VENTANA - self.fondo.get_width()) // 2)
        y = ((ALTO_VENTANA - self.fondo.get_height()) // 2)
        self.fondo_rect = self.fondo.get_rect(x=x, y=y)

        # Botones
        self.button_group = pg.sprite.Group()
        if win:
            self.titulo = BotonConTexto(BOTON_VERDE,x+90,y+30,"VICTORIA",55,scale=2.2)
        else:
            self.titulo = BotonConTexto(BOTON_ROJO,x+90,y+30,"DERROTA",55,scale=2.2)
        separacion_x = 180
        separacion_y = 65
        y_comienzo_botones = 220
        self.replay = BotonConTexto(BOTON_AMARILLO,x+separacion_x,y_comienzo_botones,"VOLVER A JUGAR",20,scale=1.3)
        self.safe_points = BotonConTexto(BOTON_VERDE,x+separacion_x,y_comienzo_botones+separacion_y,"GUARDAR PUNTUACION",15,scale=1.3)
        self.back_menu_seleccion_nivel = BotonConTexto(BOTON_AZUL,x+separacion_x,y_comienzo_botones+separacion_y*2,"SELECCION DE NIVEL",15,scale=1.3)
        self.back_menu_principal = BotonConTexto(BOTON_AZUL,x+separacion_x,y_comienzo_botones+separacion_y*3,"MENU PRINCIPAL",20,scale=1.3)
        self.button_group.add(self.titulo)
        self.button_group.add(self.replay)
        self.button_group.add(self.safe_points)
        self.button_group.add(self.back_menu_seleccion_nivel)
        self.button_group.add(self.back_menu_principal)
    
    def update(self, eventos, game):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                lista_botones = pg.sprite.spritecollide(game.cursor.sprite, self.button_group, False)
                for boton in lista_botones:
                    if boton == self.replay:
                        game.is_running = RUNNING_GAME
                        match game.level_selected:
                            case 1:
                                game.nivel_1()
                            case 2:
                                game.nivel_2()
                            case 3:
                                game.nivel_3()
                    elif boton == self.safe_points:
                        game.is_running = GUARDANDO_PUNTUACION
                        game.menu_guardar_puntuacion.level_selected = game.level_selected
                        game.enter_menu = 0
                    elif boton == self.back_menu_principal:
                        game.is_running = MENU_PRINCIPAL
                        game.level_selected = None
                        game.enter_menu = 0
                    elif boton == self.back_menu_seleccion_nivel:
                        game.is_running = MENU_SELECCION
                        game.level_selected = None
                        game.enter_menu = 0
        
class MenuPausa:
    def __init__(self):
        #Fondo
        
        self.fondo = pg.transform.scale(pg.image.load(FONDO_BLANCO), ((ANCHO_VENTANA/6)*4.5, (ALTO_VENTANA/6)*4.5))
        x = ((ANCHO_VENTANA - self.fondo.get_width()) // 2)
        y = ((ALTO_VENTANA - self.fondo.get_height()) // 2)
        self.fondo_rect = self.fondo.get_rect(x=x, y=y)

        # Botones
        self.button_group = pg.sprite.Group()
        self.titulo = BotonConTexto(BOTON_LIMPIO,x+100,y+20,"PAUSA",55,scale=2.1)
        separacion_x = 190
        separacion_y = 60
        y_comienzo_botones = 200
        self.volver_al_juego = BotonConTexto(BOTON_VERDE,x+separacion_x,y_comienzo_botones,"CONTINUAR",25,scale=1.2)
        self.replay = BotonConTexto(BOTON_ROJO,x+separacion_x,y_comienzo_botones+separacion_y,"REINICIAR",25,scale=1.2)
        self.sonido = BotonConTexto(BOTON_AMARILLO,x+separacion_x,y_comienzo_botones+separacion_y*2,"SONIDO",25,scale=1.2)
        self.back_menu_seleccion_nivel = BotonConTexto(BOTON_AZUL,x+separacion_x,y_comienzo_botones+separacion_y*3,"SELECCION DE NIVEL",15,scale=1.2)
        self.back_menu_principal = BotonConTexto(BOTON_AZUL,x+separacion_x,y_comienzo_botones+separacion_y*4,"MENU PRINCIPAL",20,scale=1.2)
        self.button_group.add(self.titulo)
        self.button_group.add(self.volver_al_juego)
        self.button_group.add(self.replay)
        self.button_group.add(self.sonido)
        self.button_group.add(self.back_menu_seleccion_nivel)
        self.button_group.add(self.back_menu_principal)
    
    def update(self, eventos, game):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                lista_botones = pg.sprite.spritecollide(game.cursor.sprite, self.button_group, False)
                for boton in lista_botones:
                    if boton == self.volver_al_juego:
                        game.is_running = RUNNING_GAME
                    if boton == self.replay:
                        game.is_running = RUNNING_GAME
                        match game.level_selected:
                            case 1:
                                game.nivel_1()
                            case 2:
                                game.nivel_2()
                            case 3:
                                game.nivel_3()
                    elif boton == self.sonido:
                        game.is_running = CONFIGURACION_SONIDO
                        game.was_running = MENU_PAUSA
                    elif boton == self.back_menu_principal:
                        game.is_running = MENU_PRINCIPAL
                        game.level_selected = None
                        game.enter_menu = 0
                    elif boton == self.back_menu_seleccion_nivel:
                        game.is_running = MENU_SELECCION
                        game.level_selected = None
                        game.enter_menu = 0

class MenuSonido:
    def __init__(self):
        #Fondo
        self.fondo = pg.transform.scale(pg.image.load(FONDO_BLANCO), ((ANCHO_VENTANA/6)*4.5, (ALTO_VENTANA/6)*4.5))
        self.x = ((ANCHO_VENTANA - self.fondo.get_width()) // 2)
        y = ((ALTO_VENTANA - self.fondo.get_height()) // 2)
        self.fondo_rect = self.fondo.get_rect(x=self.x, y=y)

        # Variables Auxiliares
        self.select_button = 0                  # Variable que guarda el tiempo de cuando se entro al menu
        self.cooldown_select_button = 100       # Variable que pone un cooldawn para poder empezar a interactuar con el menu
        self.music_on_of = True

        # Botones
        self.button_group = pg.sprite.Group()
        self.titulo = BotonConTexto(BOTON_AMARILLO,self.x+100,y+30,"SONIDO",55,scale=2.2)
        self.bajar_sonido = Button(SOUND_DOWN,self.x+160,240,scale=2)
        self.subir_sonido = Button(SOUND_UP,self.x+370,240,scale=2)
        self.button_sound_on_off = ButtonSwitch(SOUND_ON,SOUND_OFF,self.x+255,220,scale=2)
        self.volumen = BotonConTexto(BOTON_LIMPIO_CUADRADO,self.x+255,330,"10%",20,scale=2)
        self.volver = BotonConTexto(BOTON_ROJO,self.x+210,440,"VOLVER",30,scale=1)
        
        self.button_group.add(self.titulo)
        self.button_group.add(self.bajar_sonido)
        self.button_group.add(self.subir_sonido)
        self.button_group.add(self.button_sound_on_off)
        self.button_group.add(self.volumen)
        self.button_group.add(self.volver)
    
    def update(self, eventos, game, delta_ms):
        self.select_button += delta_ms
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN and self.select_button >= self.cooldown_select_button:
                self.select_button = 0
                lista_botones = pg.sprite.spritecollide(game.cursor.sprite, self.button_group, False)
                for boton in lista_botones:
                    if boton == self.button_sound_on_off:
                        self.button_sound_on_off.switch()
                        if self.music_on_of:
                            pg.mixer.music.pause()
                            self.music_on_of = False
                        else:
                            pg.mixer.music.unpause()
                            self.music_on_of = True
                    elif boton == self.subir_sonido:
                        if game.volume <= 0.9:
                            game.volume += 0.1
                            self.volumen.update_text(f"{round(game.volume*100)}%")
                    elif boton == self.bajar_sonido:
                        if game.volume >= 0.1:    
                            game.volume -= 0.1
                            self.volumen.update_text(f"{round(game.volume*100)}%")
                    elif boton == self.volver:
                        if game.was_running == MENU_PRINCIPAL:
                            game.is_running = MENU_PRINCIPAL
                        else:
                            game.is_running = MENU_PAUSA
                        game.enter_menu = 0

class MenuPuntuaciones:
    def __init__(self):
        #Fondo
        self.fondo = pg.transform.scale(pg.image.load(FONDO_MENU_PRINCIPAL), (ANCHO_VENTANA, ALTO_VENTANA))
        
        # Auxiliares
        self.__click_level_boton = False
        self.__level_selected = None
        self.__boton_1_is_on = False
        self.__boton_2_is_on = False
        self.__boton_3_is_on = False
        self.dibujar_puntajes = False

        # Botones
        self.button_group = pg.sprite.Group()
        self.titulo = BotonConTexto(BOTON_LIMPIO,180,20,"PUNTUACIONES",45,scale=2.5)
        y_botones_nivel = 150
        self.nivel_1 = ButtonSwitchText(BOTON_AZUL,BOTON_AMARILLO,100,y_botones_nivel,"NIVEL 1",25,scale=1)
        self.nivel_2 = ButtonSwitchText(BOTON_AZUL,BOTON_AMARILLO,300,y_botones_nivel,"NIVEL 2",25,scale=1)
        self.nivel_3 = ButtonSwitchText(BOTON_AZUL,BOTON_AMARILLO,500,y_botones_nivel,"NIVEL 3",25,scale=1)
        self.volver = BotonConTexto(BOTON_ROJO,20,550,"SALIR",20,scale=0.7)
        self.button_group.add(self.titulo)
        self.button_group.add(self.nivel_1)
        self.button_group.add(self.nivel_2)
        self.button_group.add(self.nivel_3)
        self.button_group.add(self.volver)

        # Botones Puntajes
        #Fondo
        self.puntajes_group = pg.sprite.Group()
        self.fondo_puntajes = pg.transform.scale(pg.image.load(FONDO_AMARILLO), ((ANCHO_VENTANA/6)*3.2, (ALTO_VENTANA/6)*3.7))
        self.x_puntajes = ((ANCHO_VENTANA - self.fondo_puntajes.get_width()) // 2)
        self.y_puntajes = ((ALTO_VENTANA - self.fondo_puntajes.get_height()) // 2) * 1.8
        self.fondo_puntajes_rect = self.fondo_puntajes.get_rect(x=self.x_puntajes, y=self.y_puntajes)
    
    def update_buttons(self):
        if self.__level_selected == 1:
            self.nivel_1.switch()
            if self.__boton_1_is_on:
                self.__boton_1_is_on = False
            else:
                self.__boton_1_is_on = True
            if self.__boton_2_is_on:
                self.nivel_2.switch()
                self.__boton_2_is_on = False
            if self.__boton_3_is_on:
                self.nivel_3.switch()
                self.__boton_3_is_on = False
        if self.__level_selected == 2:
            self.nivel_2.switch()
            if self.__boton_2_is_on:
                self.__boton_2_is_on = False
            else:
                self.__boton_2_is_on = True
            if self.__boton_1_is_on:
                self.nivel_1.switch()
                self.__boton_1_is_on = False
            if self.__boton_3_is_on:
                self.nivel_3.switch()
                self.__boton_3_is_on = False
        if self.__level_selected == 3:
            self.nivel_3.switch()
            if self.__boton_3_is_on:
                self.__boton_3_is_on = False
            else:
                self.__boton_3_is_on = True
            if self.__boton_2_is_on:
                self.nivel_2.switch()
                self.__boton_2_is_on = False
            if self.__boton_1_is_on:
                self.nivel_1.switch()
                self.__boton_1_is_on = False
        self.__click_level_boton = False

    def imprimir_puntajes(self):
        self.puntajes_group = pg.sprite.Group()
        key = f"Nivel {self.__level_selected}"
        diccionario = fl.leer_archivo_json("puntajes.json","Puntajes")
        lista_puntajes = diccionario[key]
        x_nro = 30
        x_nombre = 90
        x_puntos = 250
        y = 20
        for i in range(len(lista_puntajes)):
            self.puntajes_group.add(BotonConTexto(BOTON_LIMPIO_CUADRADO,self.x_puntajes+x_nro,self.y_puntajes+y,f"{i+1}.",20,scale=1.1))
            self.puntajes_group.add(BotonConTexto(BOTON_LIMPIO_CHIQUITO,self.x_puntajes+x_nombre,self.y_puntajes+y,lista_puntajes[i]["nombre"],20,scale=1.5))
            self.puntajes_group.add(BotonConTexto(BOTON_LIMPIO_CHIQUITO,self.x_puntajes+x_puntos,self.y_puntajes+y,str(lista_puntajes[i]["puntaje"]),20,scale=1.5))
            y += 65

    def update(self, eventos, game):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                lista_botones = pg.sprite.spritecollide(game.cursor.sprite, self.button_group, False)
                for boton in lista_botones:
                    if boton == self.nivel_1:
                        self.__level_selected = 1
                        self.__click_level_boton = True
                    elif boton == self.nivel_2:
                        self.__level_selected = 2
                        self.__click_level_boton = True
                    elif boton == self.nivel_3:
                        self.__level_selected = 3
                        self.__click_level_boton = True
                    elif boton == self.volver:
                        game.is_running = MENU_PRINCIPAL
                        game.enter_menu = 0
                if self.__click_level_boton:
                    self.update_buttons()
                    self.dibujar_puntajes = True
                    self.imprimir_puntajes()

class MenuGuardarPuntuacion:
    def __init__(self):
        #Fondo
        
        self.fondo = pg.transform.scale(pg.image.load(FONDO_BLANCO), ((ANCHO_VENTANA/6)*4.5, (ALTO_VENTANA/6)*4.5))
        x = ((ANCHO_VENTANA - self.fondo.get_width()) // 2)
        y = ((ALTO_VENTANA - self.fondo.get_height()) // 2)
        self.fondo_rect = self.fondo.get_rect(x=x, y=y)

        # Botones
        self.button_group = pg.sprite.Group()
        self.titulo = BotonConTexto(BOTON_LIMPIO,x+100,y+30,"GUARDAR PUNTUACION",25,scale=2.1)
        separacion_x = 190
        separacion_y = 60
        y_comienzo_botones = 200
        self.aceptar = BotonConTexto(BOTON_VERDE,x+separacion_x,y_comienzo_botones,"ACEPTAR",25,scale=1.2)
        self.cancelar = BotonConTexto(BOTON_ROJO,x+separacion_x,y_comienzo_botones+separacion_y,"CANCELAR",25,scale=1.2)
        self.button_group.add(self.titulo)
        self.button_group.add(self.aceptar)
        self.button_group.add(self.cancelar)
    '''
        # Botones Puntajes
        #Fondo
        self.puntajes_group = pg.sprite.Group()
        self.fondo_puntajes = pg.transform.scale(pg.image.load(FONDO_AMARILLO), ((ANCHO_VENTANA/6)*3.2, (ALTO_VENTANA/6)*3.7))
        self.x_puntajes = ((ANCHO_VENTANA - self.fondo_puntajes.get_width()) // 2)
        self.y_puntajes = ((ALTO_VENTANA - self.fondo_puntajes.get_height()) // 2) * 1.8
        self.fondo_puntajes_rect = self.fondo_puntajes.get_rect(x=self.x_puntajes, y=self.y_puntajes)

        self.level_selected = None
    
    def imprimir_puntajes(self):
        self.puntajes_group = pg.sprite.Group()
        key = f"Nivel {self.level_selected}"
        diccionario = fl.leer_archivo_json("puntajes.json","Puntajes")
        lista_puntajes = diccionario[key]
        x_nro = 30
        x_nombre = 90
        x_puntos = 250
        y = 20
        for i in range(len(lista_puntajes)):
            self.puntajes_group.add(BotonConTexto(BOTON_LIMPIO_CUADRADO,self.x_puntajes+x_nro,self.y_puntajes+y,f"{i+1}.",20,scale=1.1))
            self.puntajes_group.add(BotonConTexto(BOTON_LIMPIO_CHIQUITO,self.x_puntajes+x_nombre,self.y_puntajes+y,lista_puntajes[i]["nombre"],20,scale=1.5))
            self.puntajes_group.add(BotonConTexto(BOTON_LIMPIO_CHIQUITO,self.x_puntajes+x_puntos,self.y_puntajes+y,str(lista_puntajes[i]["puntaje"]),20,scale=1.5))
            y += 65

    '''

    def update(self, eventos, game):
        for evento in eventos:
            if evento.type == pg.MOUSEBUTTONDOWN:
                lista_botones = pg.sprite.spritecollide(game.cursor.sprite, self.button_group, False)
                for boton in lista_botones:
                    if boton == self.cancelar:
                        game.is_running = RUNNING_POST_GAME
                        game.enter_menu = 0