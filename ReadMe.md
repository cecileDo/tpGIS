# MS BigData - Stockage et traitement de données à grande échelle

## Introduction aux Systèmes d'Information Géographiques – TP OpenStreetMap

Cécile Boukamel-Donnou
__________________

Vous trouverez ci-dessous mes réponses Au TP OpenStreetMap ainsi que le code et les résultats obtenus.

## 2.1 Connexion à la base avec le client psql

```shell

 psql -U boukamec -d osm -h postgresql.ensimag.fr

```

>Question 1 : Pour vérifier que vous avez bien accès aux tables en interrogation, effectuez une requête pour compter le nombre de nœuds pour les données de la région Rhône-Alpes (= nombre de tuples de la relation nodes)

```sql
osm=> select count(*) from nodes;
  count
----------
 40247801
(1 row)
```

## 2.2 Interrogation de base

>Dans la base de données OSM, le centre de la ville de Grenoble est un nœud portant l'identifiant 26686589.  
>Question 2.a : Quelles sont ses coordonnées géographiques ?

```sql
osm=> select ST_X(geom), ST_Y( geom),GeometryType(geom),ST_SRID(geom) from nodes where id=26686589;
   st_x    |    st_y    | geometrytype | st_srid
-----------+------------+--------------+---------
 5.7357819 | 45.1875602 | POINT        |    4326
(1 row)
```

>Question 2.b : Dans quel système de référence ces coordonnées sont-elles exprimées ?

```sql
osm=> select * from spatial_ref_sys where srid=4326;
 srid | auth_name | auth_srid |                                                                                                                              srtext
                                                                                                                       |              proj4text
------+-----------+-----------+-------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------+--------------------------------------
 4326 | EPSG      |      4326 | GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Green
wich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]] | +proj=longlat +datum=WGS84 +no_defs
(1 row)

```

Le champ srtext nous donne les informations suivantes:

Le system de référence est le sytème de coordonnés WGS_84, utilisant l'ellipsoïde de référence WGS 84 de rayon 6378137m et d'applatissement inversé:298.257223563.

```txt
  SPHEROID["WGS 84",6378137,298.257223563, 
          AUTHORITY["EPSG","7030"]],
```

Le meridien de référence est greenwich

```txt
    PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],
```

L'unité est le degres correspondant à 0.0174532925199433 radians.

```txt
UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],
```

## 2.3 Interrogation attributaire (hstore)

>Question 3 : Quelles sont les coordonnées géographiques du centroïde de la mairie de Meylan (la mairie est un chemin qui contient l'attribut "amenity"=>"townhall" et dont le nom contient "Meylan".

```sql
select st_x(st_Centroid(bbox)), st_y(st_Centroid(bbox)), st_x(st_Centroid(linestring)), st_y(st_Centroid(linestring)) from ways WHERE tags->'amenity' = 'townhall' and tags->'name' LIKE '%Meylan%';
   st_x   |   st_y    |       st_x       |       st_y
----------+-----------+------------------+------------------
 5.777747 | 45.209997 | 5.77771745647958 | 45.2100224340397
(1 row)
```

>Question 4 : Compter le nombre de routes (chemins contenant la clef "highway") par type (par valeur de l'attribut "highway"), ordonné par ordre décroissant.

```sql
osm=> select count(*) sum , name from (select tags->'highway' as name from ways where  tags?'highway'
) high group by name order by sum desc;
  sum   |      name
--------+----------------
 180077 | service
 133877 | residential
 126098 | track
 107225 | unclassified
  65459 | path
  64191 | footway
  35486 | tertiary
  29179 | secondary
  18977 | primary
   8776 | steps
   6156 | pedestrian
   5719 | platform
   4804 | cycleway
   3289 | motorway
   2949 | motorway_link
   2504 | living_street
   1591 | trunk
   1441 | trunk_link
    857 | primary_link
    691 | bus_stop
    605 | road
    498 | secondary_link
    459 | tertiary_link
    350 | construction
    289 | via_ferrata
    283 | raceway
    251 | bridleway
     97 | rest_area
     83 | corridor
     68 | services
     57 | proposed
     42 | escape
     29 | elevator
     12 | yes
      6 | abandoned
      5 | bus_guideway
      4 | virtual
      2 | no
      1 | disused
      1 | closed
(40 rows)
```

## 2.4 Fonctions de mesure

>Question 5.a : Même question que précédemment (question 4), mais au lieu de compter les routes, affichez leur longueur.

```sql
osm=> select sum(length) sum , high.name from (select tags->'highway' as name, ST_Length(linestring) as length from ways where  tags?'highway'
) high group by name order by sum desc;
         sum          |      name
----------------------+----------------
     622.367870712695 | track
     505.521367103582 | unclassified
     321.179666953473 | path
     243.584404659227 | residential
     209.966466423855 | tertiary
     152.997657951426 | service
     123.373228471219 | secondary
     57.8211698512288 | footway
     54.2327259247547 | primary
     28.0227362690048 | motorway
     15.9390561330557 | cycleway
     7.95272556956238 | trunk
      6.6988974487192 | pedestrian
     5.74210030286547 | motorway_link
     3.07656081986131 | living_street
     2.61739767291822 | trunk_link
     1.77004868559225 | road
     1.65018994542522 | steps
     1.42181540641305 | raceway
     1.14852656818237 | bridleway
     1.08166831011779 | platform
     1.00440473672691 | primary_link
    0.928652651472753 | proposed
    0.870481291302807 | construction
      0.8539717893738 | services
     0.71100100084657 | rest_area
    0.497768722317564 | corridor
    0.358590701665747 | secondary_link
    0.267890500476567 | via_ferrata
    0.254636273022008 | tertiary_link
    0.124406419049083 | bus_stop
   0.0580660660501235 | escape
   0.0148991869454956 | yes
   0.0122528873879119 | abandoned
  0.00328592155896916 | elevator
  0.00278007659847706 | closed
   0.0022216036176387 | bus_guideway
  0.00202888923487431 | virtual
 0.000944443600671946 | disused
  0.00046568298372008 | no
```

>Question 5.b : En quelle unité cette longueur est-elle exprimée ?

L'unité de mesure est celle du système de référence spacial de la géometrie soit le degree. Obtenu par la requête suivante:

```sql
osm=> select ref.* from spatial_ref_sys ref , ways where ref.srid = st_srid(ways.linestring) limit 1;
 srid | auth_name | auth_srid |                                                                                                                              srtext
                                                                                                                       |              proj4text
------+-----------+-----------+-------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------+--------------------------------------
 4326 | EPSG      |      4326 | GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Green
wich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]] | +proj=longlat +datum=WGS84 +no_defs
(1 row)
```

>Question 5.c : Même question, mais avec toutes les longueurs converties dans le système métrique (km si possible).

```sql
osm=> select sum(length)/1000 sum , high.name from (select tags->'highway' as name, ST_Length(st_transform(linestring,2154)) as length from ways where  tags?'highway'
) high group by name order by sum desc;
        sum         |      name
--------------------+----------------
        sum         |      name      
--------------------+----------------
   57135.8888048645 | track
   46252.7721993421 | unclassified
   29555.7292230918 | path
   22244.7669417918 | residential
   19238.9247215731 | tertiary
   13984.4865432088 | service
   11295.1514380893 | secondary
   5269.64903683497 | footway
   4979.53268118696 | primary
   2579.98767079513 | motorway
   1462.71607832671 | cycleway
   728.625869837744 | trunk
   610.226408508155 | pedestrian
   522.730898822365 | motorway_link
   280.675563429296 | living_street
   239.690292393312 | trunk_link
   161.345976590544 | road
   149.416798108059 | steps
   127.052284762369 | raceway
   104.805778419104 | bridleway
   99.0417666968557 | platform
   91.4634267250772 | primary_link
   81.0183823578784 | proposed
   80.7650135122162 | construction
   78.5597333663787 | services
   66.2383131356414 | rest_area
   44.8084265990162 | corridor
    32.421177059444 | secondary_link
   24.2416043747991 | via_ferrata
   22.9544616426548 | tertiary_link
    11.500088227114 | bus_stop
   5.30226278717391 | escape
   1.40219531703355 | yes
   1.01936139119229 | abandoned
   0.30138712958488 | elevator
  0.264734641883629 | closed
  0.206361015221086 | bus_guideway
  0.182221786449351 | virtual
 0.0857886676627413 | disused
  0.038589117601568 | no
(40 rows)
```

Remarque: J'ai choisi la transformation EPSG:2154 qui correspond la projection Lambert-93 projection connique conforme assez précis dans les mesures pour la France metropolitaine. Cette projection ayant pour unité de mesure le mètre, les résultats sont divisés par 1000 afin d'obtenir des kilomètres.  

>Question 6 : Quelle est l'aire totale des bâtiments l'Ensimag en m2 ?

```sql
osm=> SELECT Sum(ST_Area(ST_transform(bbox, 2154)))  FROM ways WHERE tags->'operator' = 'Ensimag' ;
       sum        
------------------
 4199.24892124308
(1 row)
```

Remarque : cette aire n'est pas tout a fait correcte puisque les batiment D et H y sont représentés plusieurs fois, comme le montre la requete suivante:

```sql
osm=> SELECT tags->'name' , ST_Area(ST_transform(bbox, 2154)), tstamp  FROM ways WHERE tags->'operator' = 'Ensimag' ;
 ?column? |     st_area      |       tstamp        
----------+------------------+---------------------
 E        | 653.815239715934 | 2018-09-27 11:49:36
 Amphi D  |  1030.9509248293 | 2019-01-31 07:59:02
 H        | 640.483666984818 | 2019-08-17 09:05:46
 D        | 1432.96395606795 | 2018-09-27 11:49:45
 H        | 441.035133645078 | 2019-07-23 11:29:14
(5 rows)
```

## 2.5 Intersections, etc

>Question 7 : Affichez l'ensemble des quartiers de Grenoble, avec, pour chaque quartier, le nombre d'écoles ("amenity"=>"school") qu'il contient, le tout ordonné par nombre d'écoles décroissant.

```sql
osm=> select quartier , st_srid(geom) from quartier;
       quartier       | st_srid 
----------------------+---------
 ABBAYE-JOUHAUX       |    2154
```

la géometrie des quartiers a pour identifiant 2154 (correspondant à la projection Lambert-93 ) Pour faire des jointures avec les objets de la table  ways (en WGS84) il faut donc les convertir.

```sql
 SELECT quartier ,  count(ways.*) AS nb_shool FROM quartier, ways WHERE  ST_Contains(quartier.geom,st_transform(ways.bbox, 2154)) AND ways.Tags->'amenity' = 'school' group by quartier;
        quartier       | nb_shool 
----------------------+----------
 MALHERBE             |        3
 ALPINS-ALLIERS       |        4
 BERRIAT ST BRUNO     |       13
 ABBAYE-JOUHAUX       |        5
 CAPUCHE GR           |        2
 RONDEAU-LIBERATION   |        6
 VILLENEUVE1          |        2
 EAUX CLAIRES         |        4
 ILE VERTE            |        1
 EXPOSITION-BAJATIERE |        9
 VILLAGE-OLYMPIQUE    |        3
 VILLENEUVE2          |        2
 CENTRE VILLLE        |        3
 SAINT-LAURENT        |        1
 MUTUALITE            |        2
 JEAN MACE            |        3
 TEISSEIRE            |        1
 NOTRE DAME           |        4
(18 rows)
```

## 2.6 Des requêtes spatiales hardcore (bonus)

> Question 8 : Centre géographique de la région Rhône-Alpes. Quelle municipalité (ville, village) constitue le centre géographique de la région ?
le node Auvergne-Rhône-Alpes contient une geometry nous allons prendre celle ci-comme centre de la région (arbitrairement)

```sql
SELECT r.tags->'name' AS name , st_distance(st_transform(tn.geom,2154),pts) as dist
    FROM relations r , relation_members m ,nodes tn, 
    (select st_transform(geom,2154) as pts from  nodes where tags->'name'='Auvergne-Rhône-Alpes' 
    AND tags->'admin_level'= '4') as n 
    WHERE  r.id= m.relation_id AND  m.member_id = tn.id
    AND  r.tags->'boundary'='administrative' 
    AND r.tags->'admin_level'='8'
    order by dist asc limit 5;

           name           |       dist       
--------------------------+------------------
 Savas                    | 2465.70846927161
 Saint-Clair              | 2609.06001689862
 Saint-Marcel-lès-Annonay | 2898.34203959702
 Boulieu-lès-Annonay      | 2963.59621095525
 Brossainc                | 4000.48439318454
(5 rows)
```

Salvas est donc la commune la plus proche de la géométrie définie pour le point 'Auvergne-Rhône-Alpes'.

>Question 9 : Déserts de population. Vous voulez partir en vacances tranquillement. Existe-t-il un endroit en région Rhône-Alpes éloigné de plus de 10 kilomètres d'un bâtiment ?

On va ici restreindre les "endroits" a l'ensemble des nodes.  
Un bâtiment est considéré comme une way ayant le tag 'building' instancié.  

```sql
SELECT n.name, w.name, st_distance(n.pt, w.pt) AS dist
FROM 
  (SELECT nodes.tags->'name' AS name ,st_transform(geom,2154) AS pt
      FROM nodes ) AS n,
  (SELECT tags->'name' AS name, st_transform (linestring,2154) AS pt 
      FROM ways where tags? 'building') AS w
ORDER BY dist ASC
LIMIT 5;
```

Cette requete n'est pas du tout optimisée et ne m'a pas revoyé de résultats dans un temps "acceptable". Il y a surement mieux a faire comme calculer uniquement les distances des routes les plus proches des noeud candidats.
