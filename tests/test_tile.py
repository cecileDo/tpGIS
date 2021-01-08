import os
import sys
sys.path.append( os.path.join( os.path.dirname(__file__), '..','osm','server')) 
from osm.server import tile

def test_get_color():
    assert tile.get_color("cycleway")== (0,255,0,1)

def test_get_size_peak():
    assert tile.get_size_peak(200)== 100

if __name__ == '__main__':
    test_get_color()
    test_get_size_peak()
    print('Everything passed')