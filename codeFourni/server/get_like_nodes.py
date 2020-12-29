## reponse à la question 10
import sys
import codeFourni.server.database

def get_like_nodes(regexp):
    like_val = f'{regexp}'
    request = f"""select tags->'name', ST_x(geom), ST_y(geom) from nodes where tags->'name' like %s;"""
    cursor = database.execute_query(request, like_val)
    for row in cursor:        
        print( row )

    cursor.close()
    database.close_connection()
