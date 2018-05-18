import scrapy
from scrapy.shell import inspect_response

import logging

import pandas as pd


class CommentCrawler(scrapy.Spider):
    name = "comment_crawler"

    # Get links from the datasets
    def start_requests(self):

        # Links from search
        links = pd.read_csv('../../data/schools_via_search_categories.csv')
        search_links = links['school link'].tolist()

        # Links from listings
        links = pd.read_csv('../../data/schools_via_listing.csv')
        listings_links = links['school link'].tolist()

        # Gather all unique lnks
        all_links = list(set(search_links + listings_links))
        for url in all_links:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        print(response.url)
#
#         comment_container = response.xpath('//div[@id="content"]//div[@class="leftColumn"]')
#         comment_divs = comment_container.xpath('.//div[@class="reviewcomment"]')
#         num_comments = len(comment_divs)
#
#         # Name of school
#         school = response.xpath('//h1[@id="uname"]/text()').extract_first()
#
#         # Extract comments
#         for comment_div in comment_divs:
#             comment = comment_div.xpath('div[2]/text()').extract_first()
#             print("")
#             yield {
#                 'school': school,
#                 'comment': comment
#             }
#
#         # Check next page of comments via recusion
#         page_url = response.meta['page_url']
#         page_num = response.meta['page_num']
#         if num_comments > 0:
#             next_request = scrapy.Request(page_url + '?page=' + str(page_num), callback=self.parse_reviews)
#             next_request.meta['page_url'] = page_url
#             next_request.meta['page_num'] = page_num + 1
#             yield next_request
