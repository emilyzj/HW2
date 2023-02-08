# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/76331-succession']

    def parse(self, response):
        # navigate to cast page
        cast = response.css('li.new_button a::attr(href)').get()
        if cast:
            yield response.follow(cast, callback = self.parse_full_credits)        


    def parse_full_credits(self, response):
        actor = response.css('li.data_order a::attr(href').get()
        if actor:
            yield response.follow(actor, callback = self.parse_actor_page)


    def parse_actor_page(self, response):
        # get actor's name 
        actor_name = response.css('h2.title::text').get()

        # get movie/tv names
        for movie in response.css('.tooltip'):
            name = response.css('h2.title').get()
            yield {
                "actor": actor_name,
                "movie_or_tv_name": name
            }