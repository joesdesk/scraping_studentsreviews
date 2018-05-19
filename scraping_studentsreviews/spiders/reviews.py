# -*- coding: utf-8 -*-
import scrapy


class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['http://www.studentsreview.com']
    start_urls = ['http://http://www.studentsreview.com/viewprofile.php3?k=1481839588&u=912/']

    def parse(self, response):
        pass
