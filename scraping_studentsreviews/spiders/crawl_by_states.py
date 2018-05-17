import scrapy
from scrapy.shell import inspect_response

import logging


class StatesSpider(scrapy.Spider):
    name = "crawl_by_states"

    # Page with links to reviews for schools by state
    start_urls =[
        'http://www.studentsreview.com/college-search/lists-of-colleges-in-state.php3',
        'http://www.studentsreview.com/college-search/lists-of-colleges-in-city.php3'
        ]


    # Initial Parser
    def parse(self, response):
        page_url = 'http://www.studentsreview.com/college-search/colleges-in-New%20York'
        request = scrapy.Request(page_url + '?page=1', callback=self.parse_search_results)
        request.meta['page_url'] = page_url
        request.meta['page_num'] = 1
        yield request


    # Parse the page with links
    def parse_categ_list(self, response):

        list_container = response.xpath('//div[@id="content"]//div[@class="leftColumn"]')
        link_nodes = list_container.css('.leftColumn > a')

        for link_node in link_nodes:
            categ_name = link_node.xpath('text()').extract_first()
            categ_page = link_node.xpath('@href').extract_first()

            print(categ_name, categ_page)

            for page_url in categ_page:
                page_num = 1
                request = scrapy.Request(page_url + '?page=' + str(page_num), callback=self.parse_search_results)
                request.meta['page_url'] = page_url
                request.meta['page_num'] = 1
                yield request


    def parse_search_results(self, response):
        '''Given a page of search results, go to each result and extract the comments'''
        #inspect_response(response, self)
        url = response.url
        page_url = response.meta['page_url']
        page_num = response.meta['page_num']

        # Obtain the link to the comments page for each result
        result = response.xpath('//table[@class="searchresults"]//td[@class="resultschool"]')

        school_names = result.xpath('div/a[1]/text()').extract()
        school_links = result.xpath('div//a/@href').extract()
        valid_school_links = [l for l in school_links if l.endswith('_comments.html')]

        #
        print(school_names, valid_school_links)
        yield {
            'school_names': school_names,
            'schol_links': valid_school_links
        }
        #self.logger.info('Parse function called on %s', response.url)

        # Check next page
        if len(school_names) > 0:
            page_num += 1
            request = scrapy.Request(page_url + '?page=' + str(page_num), callback=self.parse_search_results)
            request.meta['page_url'] = page_url
            request.meta['page_num'] = page_num
            yield request


    def parse_reviews(self, response):
        pass
