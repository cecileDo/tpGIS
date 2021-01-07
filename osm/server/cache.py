

import database
import drawer
import json
import os

from pathlib import Path
from tile import Tile


class Cache:
    '''
    cette gère le cache de tuile
    '''

    def __init__(self, dir):
        self.dir=dir
        if not os.path.exists(dir):
            os.makedirs(dir)
        self.road_path = os.path.join(dir, "roads")
        if not os.path.exists(self.road_path):
            os.makedirs(self.road_path)
        self.peaks_path = os.path.join(dir, "peaks")
        if not os.path.exists(self.peaks_path):
            os.makedirs(self.peaks_path)

    def get_tile(self,layers, x_min ,y_min,x_max,y_max,srid,width, height ):
        '''
        get tile in the cache or get adn add in cache
        '''
        tileFile = self.get_tileFileName(layers, x_min ,y_min,x_max,y_max,srid,width, height )
        if not os.path.exists(tileFile):
            a_tile = Tile(x_min=x_min, y_min=y_min, x_max= x_max,y_max= y_max, 
                srid=srid, width= width,height=height)
            if layers=="peaks":
                a_tile.get_peaks()
            else:
                a_tile.get_highway()                
            self.set_tile(tileFile,a_tile.img) 
            a_tile.img.save(tileFile)
        return tileFile



    def set_tile(self,tileFile, img ):
        '''
        get tile in the cache or get adn add in cache
        '''
        img.save(tileFile)     

     
    def get_tileFileName(self,layers, x_min ,y_min,x_max,y_max,srid,width, height):
        fileName= f"{x_min}_{y_min}_{x_max}_{y_max}_{srid}_{width}_{height}"
        mytile = Path(f"{self.dir}/{layers}/{fileName.replace('.','-')}.PNG")
        print (f"Image save to {mytile}")
        return mytile