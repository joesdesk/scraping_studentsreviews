import scrapy
from scrapy.shell import inspect_response

import logging


class ViaSearchSpider(scrapy.Spider):
    name = "via_search"

    # These pages link to various search results by category,
    # from which we will extract links to the school page.
    start_urls =[
        'http://www.studentsreview.com/college-search/lists-of-colleges-in-state.php3',
        'http://www.studentsreview.com/college-search/lists-of-colleges-in-city.php3',
        ]


    # Parse the page with links by category to search pages
    def parse(self, response):

        list_container = response.xpath('//div[@id="content"]//div[@class="leftColumn"]')
        links_to_search_results = list_container.xpath('a')

        for link in links_to_search_results:
            search_query = link.xpath('text()').extract_first()
            search_results_page = link.xpath('@href').extract_first()

            print(search_query, search_results_page)

            # Extract the page for the category
            request = scrapy.Request(search_results_page + '?page=1',
                                     callback=self.parse_search_results)
            request.meta['page_url'] = search_results_page
            request.meta['page_num'] = 1
            yield request


    def parse_search_results(self, response):
        '''Given a page of search results,
        go to each result and obtain the links to each institution.'''

        # Obtain the link to the comments page for each result
        results = response.xpath('//table[@class="searchresults"]//td[@class="resultschool"]')

        for result in results:
            school_page = result.xpath('div/a[1]/text()').extract_first()
            school_link = result.xpath('div/a[1]/@href').extract_first()

            yield {'school page': school_page,
                   'school link': school_link }

        # Check next page of results via recursion
        page_url = response.meta['page_url']
        page_num = response.meta['page_num']
        if len(results) > 0:
            page_num += 1
            next_request = scrapy.Request(page_url + '?page=' + str(page_num),
                                          callback=self.parse_search_results)
            next_request.meta['page_url'] = page_url
            next_request.meta['page_num'] = page_num + 1
            yield next_request
