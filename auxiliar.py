import pygame as pg
import json

class SurfaceManager:
    @staticmethod
    def get_surface_from_spritesheet(img_path: str, cols: int, rows: int, step = 1, flip: bool = False) -> list[pg.surface.Surface]:
        sprites_list = list()
        surface_img = pg.image.load(img_path)
        frame_width = int(surface_img.get_width()/cols)
        frame_height = int(surface_img.get_height()/rows)

        for row in range(rows):

            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height

                frame_surface = surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                )

                if flip:
                    frame_surface = pg.transform.flip(frame_surface, True, False)
                sprites_list.append(frame_surface)
        return sprites_list
    
    @staticmethod
    def getSurfaceFromSeparateFiles(path_format,from_index,quantity,flip=False,scale=1,w=0,h=0,repeat_frame=1):
        lista = []
        for i in range(from_index,quantity+from_index):
            path = path_format.format(i)
            surface_fotograma = pg.image.load(path)
            fotograma_ancho_scaled = int(surface_fotograma.get_rect().w * scale)
            fotograma_alto_scaled = int(surface_fotograma.get_rect().h * scale)
            if(scale == 1 and w != 0 and h != 0):
                surface_fotograma = pg.transform.scale(surface_fotograma,(w, h)).convert_alpha()
            if(scale != 1):
                surface_fotograma = pg.transform.scale(surface_fotograma,(fotograma_ancho_scaled, fotograma_alto_scaled)).convert_alpha() 
            if(flip):
                surface_fotograma = pg.transform.flip(surface_fotograma,True,False).convert_alpha() 
            
            for i in range(repeat_frame):
                lista.append(surface_fotograma)
        return lista
    
    @staticmethod
    def getSurfaceFromFile(path,flip=False,scale=1,w=0,h=0):
        surface_fotograma = pg.image.load(path)
        fotograma_ancho_scaled = int(surface_fotograma.get_rect().w * scale)
        fotograma_alto_scaled = int(surface_fotograma.get_rect().h * scale)
        if(scale == 1 and w != 0 and h != 0):
            surface_fotograma = pg.transform.scale(surface_fotograma,(w, h)).convert_alpha()
        if(scale != 1):
            surface_fotograma = pg.transform.scale(surface_fotograma,(fotograma_ancho_scaled, fotograma_alto_scaled)).convert_alpha() 
        if(flip):
            surface_fotograma = pg.transform.flip(surface_fotograma,True,False).convert_alpha() 
            
        return surface_fotograma

class FilesManager:
    @staticmethod
    def leer_archivo_json(nombre_file:str,key) -> list:
        '''
        Leera un archivo json y devolvera la lista que hay en la clave
        Dicho archivo se abrirá en modo lectura únicamente y retornará el equipo como una lista de diccionarios.
        Recibe por parámetro un string que indicará el nombre y extensión del archivo a leer
        Devuelve el diccionario buscado o None si no pudo
        '''
        try:
            with open(nombre_file, "r",encoding='utf-8',errors='ignore') as file:
                objeto_json = json.load(file)
                diccionario = objeto_json.get(key)                
        except:
            print("\nNo se a podido descargar la informacion")
            return None
        else:
            return diccionario