import scrapy

from scrapy.loader import ItemLoader
from ..items import QuintetItem
from itemloaders.processors import TakeFirst


class QuintetSpider(scrapy.Spider):
	name = 'quintet'
	start_urls = ['https://www.quintet.lu/en-lu']

	def parse(self, response):
		post_links = response.xpath('//div[@class="l-col-3__col"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="l-section l-section--left-alignment"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//h2[@class="c-heading__pre-title"]/text()').get()

		item = ItemLoader(item=QuintetItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
