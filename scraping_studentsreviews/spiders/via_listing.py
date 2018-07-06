import scrapy

class ViaListingSpider(scrapy.Spider):
    name = 'via_listing'

    def start_requests(self):
        '''Creates iterable of requests to perform.'''
        url = 'http://www.studentsreview.com/AL/'
        yield scrapy.Request(url=url, callback=self.parse_navbar)


    def parse_navbar(self, response):
        '''Parses the navigation bar of the webpage to find pages
        each listing the colleges in the state or foreign country.
        '''

        # University Links by state and foreign countries
        xpath = '//div[@id="content"]//div[@class="leftColumn"]/center'
        listings = response.xpath(xpath)
        links = listings.xpath('a/@href').extract()[1:]

        #
        for link in links:
            request = scrapy.Request(link, callback=self.parse_listing)
            yield request


    def parse_listing(self, response):
        '''Extract the list of universities in the page
        '''
        xpath = '//div[@id="content"]//div[@class="leftColumn"]'
        colleges = response.xpath(xpath)
        colleges_list = colleges.xpath('a/@href').extract()

        for school_link in colleges_list:
            yield {'link': school_link}
