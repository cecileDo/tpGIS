#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import tile

PORT_NUMBER = 4242


class WMSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/wms"):
            # Ici on récupère les valeurs de paramètres GET
            params = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            print(f"params : {params}")
            
            acceptedParams= ['request','layers','height','width', 'srs','bbox' ]               
            # check mandatories params
            for mandatory in acceptedParams:
                if not mandatory in params:
                    self.send_error(422, f"Parametre obligatoire manquant : {mandatory}")
            #check request GetMap
            req = params.get('request','')
            if req[0] != "GetMap":
                self.send_error(404, f"Erreur mauvaise requete reçue: {req}. La seule requete acceptée est GetMap on ")            
            bbox= params['bbox'][0].split(",")
            if len(bbox) != 4:
                self.send_error(422, f"Parametre bbox doit avoir 4 valeurs : {bbox}")
            srs = int(params['srs'][0].split(":")[1])
            mytile = tile.Tile(x_min=float(bbox[0]), y_min=float(bbox[1]), x_max= float(bbox[2]),y_max= float(bbox[3]), 
                    srid=srs, width= int(params['width'][0]) , height=int(params['height'][0]))
            mytile.get_highway()
            imgToSave = 'test_highway.png'
            mytile.img.save(imgToSave)
            self.send_png_image(imgToSave)

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
        server = HTTPServer(('', PORT_NUMBER), WMSHandler)
        print('Serveur démarré sur le port ', PORT_NUMBER)
        print('Ouvrez un navigateur et tapez dans la barre d\'url :'
              + ' http://localhost:%d/' % PORT_NUMBER)

        # Ici, on demande au serveur d'attendre jusqu'à la fin des temps...
        server.serve_forever()

    # ...sauf si l'utilisateur l'interrompt avec ^C par exemple
    except KeyboardInterrupt:
        print('^C reçu, je ferme le serveur. Merci.')
        server.socket.close()
