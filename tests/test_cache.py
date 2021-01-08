import os
import sys
sys.path.append( os.path.join( os.path.dirname(__file__), '..','osm','server')) 
from osm.server import cache

def test_get_tileFileName():
    mycache = cache.Cache('adir')
    filename=  mycache.get_tileFileName('layers', 44.45 ,5,66.22,77,5465,200, 100)
    assert str(filename)=="adir/layers/44-45_5_66-22_77_5465_200_100.PNG"



if __name__ == '__main__':
    test_get_color()
    test_get_size_peak()
    print('Everything passed')