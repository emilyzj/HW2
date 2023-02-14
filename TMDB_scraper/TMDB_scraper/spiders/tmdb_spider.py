# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/76331-succession']

    def parse(self, response):
        """
        Assumes starts on movie/TV page
        Navigates to the cast page and calls function to parse through cast page
        """

        # navigate to cast page
        cast = response.css('p.new_button a').attrib['href']
        if cast:
            cast = response.urljoin(cast)
            yield scrapy.Request(cast, callback=self.parse_full_credits)        


    def parse_full_credits(self, response):
        """
        Assumes starts on credits page
        Navigates to each actor's page and calls function to parse through each actor's page
        """
        # get list of actors
        actors = response.css('ol.people.credits:not(.crew) div.info p:first-of-type a::attr(href)').getall()
        # first we want to select the people credits, excluding people in the crew
        # we want the people credits class but not the people credits crew class
        # then we want to go to the actor's information
        # we only want to look at the first occurrence of the p element 
        # and then select the link
        # getall() gives us a list of all the actors

        
        # actors = [actor for actor in people if not actor.startswith('/tv/')]

        for actor in actors:
            yield response.follow(actor, callback=self.parse_actor_page)


    def parse_actor_page(self, response):
        """
        Assumes starts on actor's page
        Yields data on the actor and each movie or TV show they've been on
        """
        # get actor's name 
        actor_name = response.css('title::text').get()
        # get actor name from the string
        # since this gives us a string of the form "first_name last_name - The Movie Database (TMDB)"
        # we want to get rid of everything after the name
        actor_name = actor_name.split('—')[0][:-1]
        # this splits the string into a list, separating by the '—'
        # we want the name, which is the first element
        # and then we just want to ignore the last white space character in the name that we retrieve

        # get movie/tv names
        for name in response.css('div.credits_list table:first-of-type bdi::text').getall():
            yield {
                "actor": actor_name,
                "movie_or_tv_name": name
            }




    """
    p:not(.episode_count_crew)
    ol.not(.crew)
    ol.
    """