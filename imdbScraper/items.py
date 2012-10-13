# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class ImdbscraperItem(Item):
	# define the fields for your item here like:
	# name = Field()
	movie_name = Field()
	movie_id = Field()
	movie_year = Field()
	movie_rating = Field()
