# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectItem(scrapy.Item):
    title = scrapy.Field()
    channel = scrapy.Field()
    start_ts = scrapy.Field()
    film_date_long = scrapy.Field()
    film_date_short = scrapy.Field()
    genre = scrapy.Field()
    plot = scrapy.Field()
    rating = scrapy.Field()
    tmdb_link = scrapy.Field()
    release_date = scrapy.Field()
    nb_votes = scrapy.Field()
    pass
