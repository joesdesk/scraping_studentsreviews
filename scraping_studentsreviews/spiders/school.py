import scrapy
from scrapy.shell import inspect_response

import logging


class SchoolsSpider(scrapy.Spider):
    name = 'schools'

    def start_requests(self):
        '''Creates iterable of requests to perform.'''
        baseurl = 'http://www.studentsreview.com/'
        self.urls = []

        listings_url = baseurl + 'AL/'
        yield scrapy.Request(url=listings_url, callback=self.parse_navbar)

        state_search_url = baseurl + 'college-search/lists-of-colleges-in-state.php3'
        yield scrapy.Request(url=state_search_url, callback=self.parse_catlist)

        city_search_url = baseurl + 'college-search/lists-of-colleges-in-city.php3'
        yield scrapy.Request(url=city_search_url, callback=self.parse_catlist)


    def parse_navbar(self, response):
        '''Parses the navigation bar of the webpage to find pages
        each listing the colleges in the state or foreign country.
        '''
        # University Links by state and foreign countries
        xpath = '//div[@id="content"]//div[@class="leftColumn"]/center'
        listings = response.xpath(xpath)
        links = listings.xpath('a/@href').extract()[1:]

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
            request = scrapy.Request(school_link, callback=self.find_ugrad_page)
            yield request


    def parse_catlist(self, response):
        '''Given a response that contains a list of search categories,
        apply the search to find college pages.'''

        xpath = '//div[@id="content"]//div[@class="leftColumn"]'
        list_container = response.xpath(xpath)
        links_to_search_results = list_container.xpath('a')

        for link in links_to_search_results:
            search_query = link.xpath('text()').extract_first()
            search_results_page = link.xpath('@href').extract_first()

            request = self.make_paged_request(search_results_page)
            yield request


    def parse_search_results(self, response):
        '''Given a page of search results,
        go to each result and obtain the links to each institution.'''

        xpath = '//table[@class="searchresults"]//td[@class="resultschool"]'
        results = response.xpath(xpath)

        for result in results:
            school_page = result.xpath('div/a[1]/text()').extract_first()
            school_link = result.xpath('div/a[1]/@href').extract_first()

            request = scrapy.Request(school_link, callback=self.find_ugrad_page)
            yield request

        # Check next page of results via recursion
        page_url = response.meta['page_url']
        page_num = response.meta['page_num']
        if len(results) > 0:
            next_request = self.make_paged_request(page_url, page_num+1)
            yield next_request


    def make_paged_request(self, page_url, page_num=1):
        '''Returns a scrapy request with page information in the meta.'''

        page_query = '?page={:d}'.format(page_num)
        request = scrapy.Request(page_url + page_query,
            callback=self.parse_search_results)
        request.meta['page_url'] = page_url
        request.meta['page_num'] = page_num
        return request


    def find_ugrad_page(self, response):
        '''Goes to the official undergradute school page.'''

        content_xpath =".//div[@id='mainContainer']/div[@id='content']"
        header = response.xpath(content_xpath)[0]

        school_link_xpath = ".//ul[@class='schoolmenu']/li[contains(@class,'Undergrad')]/a/@href"
        school_link = header.xpath(school_link_xpath).extract_first()

        if (school_link not in self.urls) and (school_link not None):
            request = scrapy.Request(school_link, callback=self.get_infos)
            yield request

    def get_infos(self, response):
        '''Extracts school information.'''

        school_name_xpath = ".//div[@id='mainContainer']/div[@id='content']/h1[@id='uname']/text()"
        school_name = response.xpath(school_name_xpath).extract_first()

        yield {'school_name': school_name, 'school_url': response.url}
