# Projet-Big-Data-Cloud-Computing-
Mise en place d'un système pour suivre les prix sur un site concurrent
Application pour le suivi des prix des livres chez Books to Scrape
Description
Ce projet est une application qui permet d'automatiser le suivi des prix via un programme (un scraper) développé en Python, capable d'extraire les informations tarifaires de la librairie en ligne Books to Scrape. A la suite de l’extraction des données, un tableau de bord interactif est développé avec Streamlit pour afficher des informations concernant essentiellement les prix de vente de livres. Ces informations présentées sous forme visuelle permettent aux utilisateurs d’explorer divers aspects des livres, comme les catégories, les prix et la disponibilité.
## Prérequis
1.	Python 3.12.2 (il faut utiliser une version < 3.13)
2.	Bibliothèques nécessaires :
o	Scrapy
o	boto3
o	python-dotenv
o	streamlit
3.	Compte AWS avec accès à un bucket S3 et clés d’accès AWS.
4.	Fichier.env contenant les informations suivantes : le nom du bucket, la clé d’accès au bucket, la clé secrète.
## Installation
1. Cloner le projet
git clone " https://github.com/GADO-Seman-Giovanni-Jocelyn/Projet-Big-Data-Cloud-Computing-"
2. Creation de l’environnement de travail
python -m venv venv # creation
venv\Scripts\activate # activation

3. Installer les dépendances
pip install -r requirements.txt
4. Configurer les variables d'environnement :
•	Créer un fichier. env à la racine du projet et y ajouter les informations AWS.
Structure du Projet
Description de certains fichiers
•	bookscraper.py : Spider Scrapy pour extraire les informations des livres.
•	pipelines.py : Pipeline de traitement des données et chargement vers AWS S3.
•	settings.py : Configuration du projet et gestion des paramètres Scrapy.
•	.env : Stockage sécurisé des clés AWS (non inclus dans le dépôt).
Exécution du scraping
-	Afin de réaliser le scraping se placer dans dossier bookscraper( par exemple avec cd bookscraper dans le terminal)
-	Ensuite dans terminal executer: 
scrapy crawl books
Le spider parcourt le site et collecte les informations, qui sont ensuite enregistrées dans un fichier CSV. Une fois le scraping terminé, le fichier est automatiquement uploadé sur AWS S3.



