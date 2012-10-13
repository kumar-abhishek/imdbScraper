from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from imdbScraper.items import ImdbscraperItem

class ImdbSpider(BaseSpider):
	name = "imdb"
	allowed_domains = ["www.imdb.com"]
	start_urls = ["http://www.imdb.com/chart/top"]
	
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		items = []
		movie_details = hxs.select("//table//tr[@bgcolor='#e5e5e5' or @bgcolor='#ffffff']")
		for detail in movie_details:
			item = ImdbscraperItem()
			item['movie_name'] = detail.select(".//a[contains(@href, '/title/')]/text()").extract()[0]
			item['movie_id'] = detail.select(".//a[contains(@href, '/title/')]/@href").extract()[0].split('/')[2]
			item['movie_year'] = detail.select(".//font[descendant::a[contains(@href, '/title/')]]/text()").extract()[0].strip(")( ")
                        item['movie_rating'] = detail.select(".//td[@align = 'center']/font/text()").extract()[0]
			items.append(item)	
		return items
	


