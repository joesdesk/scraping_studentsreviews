import scrapy

class ViaListingSpider(scrapy.Spider):
    name = 'via_listing'

    start_urls = ['http://www.studentsreview.com/AL/']

    def parse(self, response):
        # University Links
        listings = response.xpath('//div[@id="content"]//div[@class="leftColumn"]/center')
        links = listings.xpath('a/@href').extract()[1:]

        for link in links:
            request = scrapy.Request(link, callback=self.parse_listings)
            yield request


    def parse_listings(self, response):
        colleges = response.xpath('//div[@id="content"]//div[@class="leftColumn"]')
        colleges_list = colleges.xpath('a/@href').extract()

        for school_link in colleges_list:
            yield {'school link': school_link}
