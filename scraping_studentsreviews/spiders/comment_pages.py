import scrapy
from scrapy.shell import inspect_response

import logging
import re

ugrad_regex = re.compile(r"_u.html$")
def ugrad2comment(url):
    '''Converts the link from the undergraduate page to the comments page.'''
    new_url, n_subs = ugrad_regex.subn('_comments.html', url)
    assert n_subs==1, 'Unable to convert {:s} link to comment link.'.format(url)
    return new_url


class CommentPagesCrawler(scrapy.Spider):
    name = "comment_pages"

    # Get links from the datasets
    def start_requests(self):
        '''Extracts links from files and starts the scraping process.'''

        # Collect all links from the files
        files = ['via_search.csv', 'via_listing.csv']
        for filename in files:
            links = []
            with open(filename, 'r') as f:
                assert f.readline()=='link\n', "Header of csv must be link"
                links.extend( f.readlines() )

        # Remove newlines and duplicates
        links = [l.rstrip('\n') for l in links]
        links = set(links)
        links.discard('')
        links = list(links)

        # For each college page, find the link to the comments
        self.unique_links = []
        for url in links:
            yield scrapy.Request(url=url, callback=self.find_comment_page)

    def find_comment_page(self, response):
        '''Finds the link to the comments.'''

        # Extract university name and link to undergraduate subpage
        content_xpath = ".//div[@id='mainContainer']/div[@id='content']"

        uname_xpath = content_xpath + "/h1[@id='uname']/text()"
        uname = response.xpath(uname_xpath).extract_first()

        link_xpath = content_xpath + "//ul[@class='schoolmenu']/li[contains(@class,'Undergrad')]/a/@href"
        link = response.xpath(link_xpath).extract_first()

        # Get link to first comments page
        link = ugrad2comment(link)
        if link not in self.unique_links:
            self.unique_links.append(link)
            request = self.make_paged_request(link)
            yield request


    def parse_reviews_pages(self, response):
        '''Extracts links to the full comments for each comment on the page.
        '''
        # Obtain divs containing comments
        xpath = "//div[@class='portfolioContainer']" + \
            "/div[@id='full' and contains(@class, 'reviewcomment')]" + \
            "/div/a[@class='readmore']/@href"
        fullreview_links = response.xpath(xpath).extract()

        # Get link to full review
        for l in fullreview_links:
            yield {'full_review': l}

        # Check next page of comments via recusion
        page_url = response.meta['page_url']
        page_num = response.meta['page_num']
        if len(fullreview_links) > 0:
            next_request = self.make_paged_request(page_url, page_num+1)
            yield next_request


    def make_paged_request(self, page_url, page_num=1):
        '''Returns a scrapy request with page information in the meta.'''
        page_query = '?page={:d}'.format(page_num)
        request = scrapy.Request(page_url + page_query,
            callback=self.parse_reviews_pages)
        request.meta['page_url'] = page_url
        request.meta['page_num'] = page_num
        return request
