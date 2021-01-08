#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
from psycopg2.extensions import register_adapter
import tile
import sys
import cache

PORT_NUMBER = 4242

class WMSHandler(BaseHTTPRequestHandler):

    def __init__(self, cached= False):
        """
        init if cached= true init the cache
        """
        self.cached= cached
        if cached:
            self.cache = cache.Cache("./__cache")

    def __call__(self, *args, **kwargs):
        """ Handle a request """
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path.startswith("/wms"):
            
            # Ici on récupère les valeurs de paramètres GET
            params = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            print(f"params : {params}")
                               
            # check mandatories params
            for mandatory in ['request','layers','height','width', 'srs','bbox' ] :
                if not mandatory in params:
                    self.send_error(422, f"Parametre obligatoire manquant : {mandatory}")                    
                    return

            # check request GetMap
            req = params['request'][0]
            if req != "GetMap":
                self.send_error(404, f"Erreur mauvaise requete reçue: {req}. La seule requete acceptée est GetMap")  
                
            
            # check bbox          
            bbox= params['bbox'][0].split(",")
            if len(bbox) != 4:
                self.send_error(422, f"Parametre bbox doit avoir 4 valeurs : {bbox}")

            # check layers
            layers=params['layers'][0]
            if layers not in {'roads','peaks'}:
                self.send_error(422, f"Parametre layers doit etre soit roads soit peaks : {layers}")
            # srid
            srs = params['srs'][0]
            if srs.isdigit():
               srid= srs
            else:
                srid= int(srs.split(":")[1])
            
            if self.cached:           
                mytile = self.cache.get_tile(layers=layers, x_min=float(bbox[0]), y_min=float(bbox[1]), x_max= float(bbox[2]),y_max= float(bbox[3]), 
                    srid=srid, width= int(params['width'][0]) , height=int(params['height'][0]))
            else:               
              mytile= tile.get_tile(layers=layers,x_min=float(bbox[0]), y_min=float(bbox[1]), x_max= float(bbox[2]),y_max= float(bbox[3]),
                    srid=srid, width= int(params['width'][0]) , height=int(params['height'][0]),name="atile")              
            self.send_png_image(mytile)

        self.send_error(404, 'Fichier non trouvé : %s' % self.path)

    def send_plain_text(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=UTF-8')
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))

    def send_png_image(self, filename):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_html_file(self, filename):
        self.send_response(200)
        self.end_headers()
        self.serveFile(filename)


if __name__ == "__main__":
    try:
        # Ici on crée un serveur web HTTP, et on affecte le traitement
        # des requêtes à notre releaseHandler ci-dessus.
        # si premiere argument = cache on utilise le cache
        cached = False
        if len(sys.argv) >1 and sys.argv[1]=='cached':
            print("CACHED")
            cached=True

        handler = WMSHandler(cached)
        server = HTTPServer(('', PORT_NUMBER), handler)
        print('Serveur démarré sur le port ', PORT_NUMBER)
        print('Ouvrez un navigateur et tapez dans la barre d\'url :'
              + ' http://localhost:%d/' % PORT_NUMBER)
        
        # Ici, on demande au serveur d'attendre jusqu'à la fin des temps...
        server.serve_forever()

    # ...sauf si l'utilisateur l'interrompt avec ^C par exemple
    except KeyboardInterrupt:
        print('^C reçu, je ferme le serveur. Merci.')
        server.socket.close()
