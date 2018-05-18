import scrapy

class ViaListingSpider(scrapy.Spider):
    name = 'via_listing'

    start_urls = ['http://http://www.studentsreview.com/AL/']

    def parse(self, response):
        pass
