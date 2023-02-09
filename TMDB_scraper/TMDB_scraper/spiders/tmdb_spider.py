# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/76331-succession']

    def parse(self, response):
        # navigate to cast page
        cast = response.css('p.new_button a').attrib['href']
        if cast:
            cast = response.urljoin(cast)
            yield scrapy.Request(cast, callback=self.parse_full_credits)        


    def parse_full_credits(self, response):
        # get list of actors
        people = response.css('div.info:not(.crew) a::attr(href)').getall()
        actors = [actor for actor in people if not actor.startswith('/tv/')]

        for actor in actors:
            yield response.follow(actor, callback=self.parse_actor_page)


    def parse_actor_page(self, response):
        # get actor's name 
        actor_name = response.css('title::text').get()
        # get actor name from the string
        actor_name = actor_name.split('—')[0][:-1]

        # get movie/tv names
        for name in response.css('a.tooltip bdi::text').getall():
            yield {
                "actor": actor_name,
                "movie_or_tv_name": name
            }