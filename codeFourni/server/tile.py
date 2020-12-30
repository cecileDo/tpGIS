import database
import drawer

colorRgba={'red':(255,0,0,1),'pink':(255, 0, 3, 0.3), 'black' :(0,0,0,1) , 'grey' :(0,0,0,0.5), 'green' :(0,255,0,1),'blue' :(0, 226, 255, 0.6), 'yellow':(255, 255, 3, 1) }

class Tile:
    '''
    cette classe cree une tuile
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
        self.yFactor = height/(y_max-y_min)
        self.x_offset = -x_min #*self.xFactor
        self.y_offset = -y_min #*self.yFactor
        self.img =drawer.Image(width, height)
        print ( f" factors x {self.xFactor} max :{x_max} min {x_min} y: {self.yFactor} max :{y_max} min {y_min} ")


    def get_highway(self ):
        '''
        get all highway in box with point
        '''

        request = f"""select TransScale(ST_transform(linestring,%s),%s,%s,%s,%s), tags->'highway' from ways where tags?'highway' and   
        ST_MakeEnvelope (
            %s, %s, 
            %s, %s, 
            %s) ~ ST_transform(linestring,%s) ;"""    
        cursor = database.execute_query(request,self.srid ,self.x_offset,self.y_offset, self.xFactor,self.yFactor,self.x_min, self.y_min,self.x_max, self.y_max,self.srid ,self.srid )

        for row in cursor:
            col = get_color(row[1])
            self.img.draw_linestring(row[0],col)

        cursor.close()
        database.close_connection()

def get_color(highway):
    switcher={
            'service':'grey',
            'residential':'blue',
            'tertiary':'yellow',
            'motorway_link':'pink',
            'motorway':'red'
            }
    color=switcher.get(highway,"black")
    return colorRgba.get(color)
    
def get_highway_fixed():
    mytile = Tile(5.7, 45.1, 5.8, 45.2, 4326, 600 , 600)
    mytile.get_highway()
    imgToSave = 'test_highway.png'
    mytile.img.save(imgToSave)
    print (f"Image save to {imgToSave}")