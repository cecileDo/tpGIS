import database
import drawer
import json


colorRgba={'red':(255,0,0,1),'pink':(255, 0, 3, 0.3), 'black' :(0,0,0,1) , 
           'grey' :(0,0,0,0.5), 'green' :(0,255,0,1),'blue' :(0, 226, 255, 0.6), 
           'brown' :(104, 53, 43, 1), 'darkblue' :(0, 226, 255, 0.6),
           'yellow':(255, 255, 3, 1), 'orange':(255, 114, 80, 0.4) }

class Tile:
    '''
    cette classe cree une tuile
    a partir des donnés comprises dans la "boite" 
    délimitées par les self.x_min, self.y_min, self.x_max, self.y_max exprimées en self.srid 
    '''

    def __init__(self, x_min ,y_min,x_max,y_max,srid,width, height):
        self.x_min= x_min
        self.y_min= y_min
        self.x_max=x_max
        self.y_max= y_max
        self.srid = srid
        self.width= width
        self.height= height
        self.xFactor = width/(x_max-x_min)
        self.yFactor = -height/(y_max-y_min) 
        self.x_offset = -x_min *self.xFactor
        self.y_offset = -y_min*self.yFactor + height 
        self.img =drawer.Image(width, height)
        print ( f" factors x {self.xFactor} max :{x_max} min {x_min} y: {self.yFactor} max :{y_max} min {y_min} ")


    def get_highway(self ):
        '''
        create a tile with highway
        situates in box delimitted by self.x_min, self.y_min, self.x_max, self.y_max in exprimed in self.srid 
        coordinates are projected  
            x = x * self.xFactor + self.x_offset
            y = y * self.yFactor + self.Y_offset
        '''
        
        request = f"""select ST_Affine(ST_transform(linestring,%s),%s,0,0,%s,%s,%s), tags->'highway' from ways where tags?'highway' and   
        ST_transform(ST_MakeEnvelope (
            %s, %s, 
            %s, %s, 
            %s),4326) ~ linestring ;"""  
        cursor = database.execute_query(request,self.srid, self.xFactor,self.yFactor ,self.x_offset,self.y_offset,self.x_min, self.y_min,self.x_max, self.y_max,self.srid )

        for row in cursor:
            col = get_color(row[1])
            self.img.draw_linestring(row[0],col)

        cursor.close()
        database.close_connection()

    def get_peaks(self ):
        '''
        create a tile with peaks coordinate elevation and name 
        situates in box delimitted by self.x_min, self.y_min, self.x_max, self.y_max in exprimed in self.srid 
        coordinates are projected  
            x = x * self.xFactor + self.x_offset
            y = y * self.yFactor + self.Y_offset
        '''
        
        request = f"""SELECT ST_X(a.geo) , ST_Y(a.geo) , a.name, a.ele FROM 
            (SELECT ST_Affine(ST_transform(geom,%s),%s,0,0,%s,%s,%s) as geo, tags->'name' as name, tags->'ele' as ele FROM nodes 
            WHERE tags?'natural' AND tags?'name' AND tags->'natural' ='peak' AND
            ST_transform(ST_MakeEnvelope (
                %s, %s, 
                %s, %s, 
                %s),4326) ~ geom ) as  a ;"""  

        cursor = database.execute_query(request,self.srid, self.xFactor,self.yFactor ,self.x_offset,self.y_offset,self.x_min, self.y_min,self.x_max, self.y_max,self.srid )

        for row in cursor:
            print(row)
            ele = row[3]
            if ele is not None:
                size = get_size_peak(int(ele))/10
            else:
                size = 1
            x=row[0]
            y=row[1]           
            self.img.draw_text(row[2],x,y,colorRgba['black'],10)
            self.img.draw_rectangle(x,y, size, size,colorRgba['blue'] , colorRgba['blue'])
           
        cursor.close()
        database.close_connection()


def get_color(highway):
    '''
    retourne la couleur des route en fonction de leur type
    '''
    switcher={
            'service':'grey',
            'residential':'blue',
            'tertiary':'black',
            'motorway_link':'red',
            'motorway':'red',
            'cycleway' :'green'
            }
    color=switcher.get(highway,"black")
    return colorRgba.get(color)

def get_size_peak(ele):
    '''
    retourne la taille de la représentation des sommets 
    en fonction de leur altitude
    '''
    size = 100
    if (ele > 3000):
        size += 135
    elif ele > 2500:
        size += 130
    elif ele > 2000:
        size += 125
    elif ele > 1500:
        size += 120
    print (f"ele: {ele}, size : {size}")
    return size

def get_highway_fixed():
    '''
    methode de test pour la fonction get_highway()
    '''
    mytile = Tile(5.7, 45.1, 5.75, 45.15, 4326, 200 , 200)
    mytile.get_highway()
    imgToSave = 'test_highway.png'
    mytile.img.save(imgToSave)
    print (f"Image save to {imgToSave}")

def get_tile(layers, x_min, y_min, x_max,y_max, 
                    srid, width, height, name):
    '''
    cree une tuile du type corresondant a la couche (layer) 
    a partir des donnés comprises dans la "boite" 
    délimitées par les self.x_min, self.y_min, self.x_max, self.y_max exprimées en self.srid 
    '''

    mytile = Tile(x_min, y_min, x_max,y_max, 
                    srid, width, height)
    
    if layers == "peaks":
        mytile.get_peaks()       
    else:
        mytile.get_highway()        
    mytile.img.save(name)
    return name
