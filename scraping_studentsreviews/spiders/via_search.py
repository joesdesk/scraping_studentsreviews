import scrapy
from scrapy.shell import inspect_response

import logging


class ViaSearchSpider(scrapy.Spider):
    name = "via_search"

    # These pages link to various search results by category,
    # from which we will extract links to the school page.
    def start_requests(self):
        '''Parses each list of search categories'''
        start_urls =[
            'http://www.studentsreview.com/college-search/lists-of-colleges-in-state.php3',
            'http://www.studentsreview.com/college-search/lists-of-colleges-in-city.php3',
            ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_catlist)


    # Parse the page with links by category to search pages
    def parse_catlist(self, response):
        '''Given a response that contains a list of search categories,
        apply the search to find college pages.'''

        xpath = '//div[@id="content"]//div[@class="leftColumn"]'
        list_container = response.xpath(xpath)
        links_to_search_results = list_container.xpath('a')

        for link in links_to_search_results:
            search_query = link.xpath('text()').extract_first()
            search_results_page = link.xpath('@href').extract_first()

            # Extract the page for the category
            request = self.make_paged_request(page_url)
            yield request


    def parse_search_results(self, response):
        '''Given a page of search results,
        go to each result and obtain the links to each institution.'''

        # Obtain the link to the comments page for each result
        xpath = '//table[@class="searchresults"]//td[@class="resultschool"]'
        results = response.xpath(xpath)

        for result in results:
            school_page = result.xpath('div/a[1]/text()').extract_first()
            school_link = result.xpath('div/a[1]/@href').extract_first()
            yield {'link': school_link}

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
