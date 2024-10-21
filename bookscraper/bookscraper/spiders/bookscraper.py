#premiere etapes localisation des url de categories, des livres et des champs de données que nous voulons
#Resultats:
#les URL de catégorie sont stockées dans un ul, élément HTML avec une classe nav nav-list
#Les URL des pages de livres individuelles sont situées sous un articleélément HTML avec la classe CSS product pod
import scrapy
import datetime

# Le spider commence par l’URL de départ et récupère tous les liens de catégories.
#Pour chaque catégorie, il visite la page de catégorie et extrait les informations sur les livres.
#Si une page suivante existe, le spider continue sur cette nouvelle page.
class bookSpider(scrapy.Spider):
    name='books'
    start_urls = ["http://books.toscrape.com/index.html"]

    def parse(self, response):
        categories= response.css('ul.nav-list ul li a::attr(href)').getall()
        for url_categorie in categories:
            full_url_categorie=response.urljoin(url_categorie)
            yield scrapy.Request(full_url_categorie,callback=self.parse_categorie)

    def parse_categorie(self, response):
        #nom de la categorie
        nom_categorie=response.css('div.page-header h1::text').get().strip()
        # date d'extraction 
        scraping_date = datetime.date.today()
        #informations sur les livres
        for book in response.css('article.product_pod'):
            yield{
                'date': scraping_date,
                'title':book.css('h3 a::attr(title)').get(),
                'categorie': nom_categorie,
                'prix': book.css('p.price_color::text').get().strip(),
                'availability':book.css('p.instock.availability::text').re_first('\w+'),
                'rating':book.css('p::attr(class)').re_first('star-rating (\w+)'),
                
            }
        # page suivante de chaque categorie
        next_page= response.css('li.next a::attr(href)').get()
        if next_page:
            url_next_page=response.urljoin(next_page)
            yield scrapy.Request(url_next_page,callback=self.parse_categorie)
            

