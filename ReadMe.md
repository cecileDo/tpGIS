# MS BigData - Stockage et traitement de données à grande échelle

## Introduction aux Systèmes d'Information Géographiques – TP OpenStreetMap -partie II python

Cécile Boukamel-Donnou
__________________

Vous trouverez ci-dessous mes réponses Au TP OpenStreetMap partie II python ainsi que le code et les résultats obtenus.

## installation

Pour installer et creer l'environement permettant d'executer les scripts du tp:

```shell
sudo apt install libcairo2-dev pkg-config python3-dev
git clone https://github.com/cecileDo/tpGIS.git
cd tpGIS
make venv
```

## reponses aux questions

Un fichier Makefile permet de rapidement jouer les réponses aux questions

>Question 10 :Écrivez un petit programme de test prenant un argument en ligne de commande, et affichant tous les noms et coordonnées géographiques des points dont le nom ressemble à (au sens du LIKE SQL) l'argument.

Le programe est disponible dans server/get_like_node.py

```shell
  make get_nodes
```

> Question 11 : Écrivez la fonction demandée, ainsi qu'un petit programme qui la teste sur la boîte englobante de longitudes comprises entre 5.7 et 5.8, et latitudes comprises entre 45.1 et 45.2, dans le système WGS84.

Le programe est disponible dans server/tile.py

```shell
   make get_highway_example
```
