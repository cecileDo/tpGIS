# MS BigData - Stockage et traitement de données à grande échelle

## Introduction aux Systèmes d'Information Géographiques – TP OpenStreetMap -partie II python

Cécile Boukamel-Donnou
__________________

Vous trouverez ci-dessous mes réponses Au TP OpenStreetMap partie II python ainsi que le code et les résultats obtenus.

## fonctionalités in finé

Cette application  permet de:

* récuperer les noms et coordonnées géographiques des points dont le nom ressemble à (au sens du LIKE SQL) l'argument

* lancer un server de tuile, avec ou sans cache qui sert des couches contenant  les routes et les sommets et un fond de carte

## achitecture

Un fichier Makefile permet de rapidement créer l'environement vituel python avec les librairies nécessaire, jouer les réponses aux questions, lancer les server

### coté server

Un server WEB qui peut-être lancé en deux modes différent: avec ou sans cache.  
Si le server est lancé sans cache, il interroge la classe **Tile** qui cree une tuile de la taille demandée, contenant les informations de la couche désirée,
à partir des donnés comprises dans la "boite" passée en paramètre et exprimées en srid.

Si le server est lancé en mode cache, il interroge la classe **Cache**. Celle-ci cheche dans son cache (répertoire contenant les images) la tuile correspondante à la demande (même boite, couche, srid, taille de tuile), si la tuile existe, elle est renvoyée, sinon elle est demandée à la classe **Tile** comme le ferait le server sans cache, puis enregistrée dans le cache avant des renvoyée.

### coté client

une page HTML instancie un contenu fourni par le script map.js  
le script map.js utilise l'api leaflet pour demander et afficher des tuiles de chaque couche de manière optimisée.

## installation

Pour installer et creer l'environement permettant d'executer les scripts du tp:

```shell
sudo apt install libcairo2-dev pkg-config python3-dev
git clone https://github.com/cecileDo/tpGIS.git
cd tpGIS
make venv
source venv/bin/activate
```

## reponses aux questions du tp

### Interrogation de la base de donnée avec psycopg2 et posgis

>Question 10 :Écrivez un petit programme de test prenant un argument en ligne de commande, et affichant tous les noms et coordonnées géographiques des points dont le nom ressemble à (au sens du LIKE SQL) l'argument.

Le programe est disponible dans le fichier python osm/server/get_like_node.py

```shell
make get_nodes 
Enter search regexp:Dom__ne _niversit%
Mes params <connection object at 0x7f8ec9bbb048; dsn: 'user=boukamec password=xxx dbname=osm host=195.221.228.252', closed: 0>, select tags->'name', ST_x(geom), ST_y(geom) from nodes where tags->'name' like %s;, ('Dom__ne _niversit%',) 

('Domaine Universitaire', 5.7588187, 45.1935807)
('Domaine Universitaire', 5.758102, 45.1874865)
('Domaine Universitaire', 5.7569834, 45.1870508)
('Domaine Universitaire', 5.7695911, 45.1881104)
('Domaine Universitaire', 5.7611708, 45.1898362)
(venv) cecile@cecile-VirtualBox:~/masterBD/tpGIS/python-osm$ 
```

### Creation d'une tuile

> Question 11 : Écrivez la fonction demandée, ainsi qu'un petit programme qui la teste sur la boîte englobante de longitudes comprises entre 5.7 et 5.8, et latitudes comprises entre 45.1 et 45.2, dans le système WGS84.

Le programe est disponible dans osm/server/tile.py.

Un exemple de résultat peut-être obtenu par:

```shell
   make get_highway_example
```

Image générée:  

![alt text](img/test_highway.png "Resultat question 11")

**Remarque sur la conception de la requete Tile.get_highway():**  
Pour faire la selection des chemins, c'est l'enveloppe construite avec les paramètre x_min y_min, x_max, y_max qui est transformée en coordonnées 4326 correspondant a celle de la géométrie des ways dans la base de donnée, et non l'inverse. Je ne savais pas quelle solution est la plus optimisée.

### Server de tuile

>Question 12 : Complétez le fichier WMSServer.py pour implanter le serveur WMS tel que décrit ci-dessus.

Pour lancer le server:

```shell
   make run_WMS
```

Le code est disponible dans osm/server/WMSserver.py.

### Server de tuile avec cache

Pour lancer le server:

```shell
   make run_WMS_cached
```

Le code est disponible dans osm/server/cache.py.
un fichier de test est sous test/test_cache.py test la methode de creationd es noms

**Remarque sur la conception du cache:**  
Chaque image générée est sauvegardée dans le repetoire osm/server/\_\_cache\_\_.  
Ce répertoire contient 2 sous répertoires "peaks" et "roads" correspondant aux couches.  

les noms de fichiers sont ensuite construits de la manière suivante:  
{x_min}_{y_min}_{x_max}_{y_max}_{srid}_{width}_{height}.PNG  
  dans lequel les '.' sont remplacés par des '-'.
par exmple:  
621280-1659019126_5635549-221409476_626172-1357121639_5640441-191219728_3857_256_256.PNG

### Nouvelle couche

Pour cet exercice, j'ai choisi de représenter les sommets, avec un rectangle plus ou moins gros selon l'altitude.
Leur noms sont aussi affichés

pour activer la couche dans le navigateur cocher la couche sommets:

![alt text](img/Rendu.png  "Resultat final")

### Annexe résultat test d'erreur du server

Tests effectués (aussi par le nevigateur mais c'est plus facile a montrer ici):

```sh
(venv) cecile@cecile-VirtualBox:~/masterBD/tpGIS/python-osm/tests$ ./test_WMSserver.sh 
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 422</p>
        <p>Message: Parametre obligatoire manquant : request.</p>
        <p>Error code explanation: 422 - .</p>
    </body>
</html>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 422</p>
        <p>Message: Parametre obligatoire manquant : layers.</p>
        <p>Error code explanation: 422 - .</p>
    </body>
</html>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 422</p>
        <p>Message: Parametre obligatoire manquant : height.</p>
        <p>Error code explanation: 422 - .</p>
    </body>
</html>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 422</p>
        <p>Message: Parametre obligatoire manquant : width.</p>
        <p>Error code explanation: 422 - .</p>
    </body>
</html>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 422</p>
        <p>Message: Parametre obligatoire manquant : srs.</p>
        <p>Error code explanation: 422 - .</p>
    </body>
</html>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 422</p>
        <p>Message: Parametre obligatoire manquant : bbox.</p>
        <p>Error code explanation: 422 - .</p>
    </body>
</html>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 404</p>
        <p>Message: Erreur mauvaise requete reçue: toto. La seule requete acceptée est GetMap.</p>
        <p>Error code explanation: 404 - Nothing matches the given URI.</p>
    </body>
</html>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 422</p>
        <p>Message: Parametre layers doit etre soit roads soit peaks : rr.</p>
        <p>Error code explanation: 422 - .</p>
    </body>
</html>
Warning: Binary output can mess up your terminal. Use "--output -" to tell 
Warning: curl to output it to your terminal anyway, or consider "--output 
Warning: <FILE>" to save to a file.
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <title>Error response</title>
    </head>
    <body>
        <h1>Error response</h1>
        <p>Error code: 400</p>
        <p>Message: Bad request syntax ('GET /wms?request=GetMap&amp;layers=roads&amp;height=20&amp;width=30&amp;srs=EPSG:3857&amp;bbox=645740.014953169,5650225.13084023,650631.9847634204,5655117.100650479 --output toto.PNG HTTP/1.1').</p>
        <p>Error code explanation: HTTPStatus.BAD_REQUEST - Bad request syntax or unsupported method.</p>
    </body>
</html>


```