#première étape localisation des url de categories, des livres et des champs de données que nous voulons
#Resultats:
#les URL de catégorie sont stockées dans un ul, élément HTML avec une classe nav nav-list
#Les URL des pages de livres individuelles sont situées sous un article élément HTML avec la classe CSS product pod

# Le spider commence par l’URL de départ et récupère tous les liens de catégories.
#Pour chaque catégorie, il visite la page de catégorie et extrait les informations sur les livres.
#Si une page suivante existe, le spider continue sur cette nouvelle page.

import scrapy
import datetime
import re

class BookSpider(scrapy.Spider):
    name = 'books'
    start_urls = ["http://books.toscrape.com/index.html"]

    def parse(self, response):
        categories = response.css('ul.nav-list ul li a::attr(href)').getall()
        for url_categorie in categories:
            full_url_categorie = response.urljoin(url_categorie)
            yield scrapy.Request(full_url_categorie, callback=self.parse_categorie)

    def parse_categorie(self, response):
        nom_categorie = response.css('div.page-header h1::text').get().strip()
        livres = response.css('article.product_pod h3 a::attr(href)').getall()
        for livre in livres:
            full_url_livre = response.urljoin(livre)
            yield scrapy.Request(full_url_livre, callback=self.parse_livre, meta={'categorie': nom_categorie})

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse_categorie)

    def parse_livre(self, response):
        nom_categorie = response.meta['categorie']
        scraping_date = datetime.date.today()
        title = response.css('div.product_main h1::text').get()
        prix_raw = response.css('p.price_color::text').get()
        prix = prix_raw.replace('£', '').strip() if prix_raw else 'N/A'
         # Nombre d'étoiles (rating)
        rating_raw = response.css('p.star-rating::attr(class)').get()
        rating = rating_raw.split()[-1]  # Extrait le dernier mot (One, Two, Three, etc.)

        # Mapping de texte vers un nombre d'étoiles
        rating_dict = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        stars = rating_dict.get(rating, 0)  # Valeur par défaut : 0


        availability_raw = response.css('table tr:contains("Availability") td::text').get()
        availability = 'In stock' if 'In stock' in availability_raw else 'Out of stock'

        disponible = 0
        if 'available' in availability_raw:
            try:
                disponible = int(re.search(r'\((\d+) available\)', availability_raw).group(1))
            except (IndexError, ValueError):
                disponible = 0

        yield {
            'date': str(scraping_date),
            'title': title,
            'categorie': nom_categorie,
            'prix': prix,
            'availability': availability,
            'nombre_de_livres_disponible': disponible,
            'rating':stars
        }
