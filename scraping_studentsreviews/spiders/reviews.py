# -*- coding: utf-8 -*-
import scrapy
#from scrapy.loader import ItemLoader
from scraping_studentsreviews.items import Review, ProductLoader

from urllib.parse import urlparse, parse_qs
# See: https://docs.python.org/3/library/urllib.parse.html


class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['studentsreview.com']
    start_urls = ['http://www.studentsreview.com/viewprofile.php3?k=1481839588&u=912',
        'http://www.studentsreview.com/viewprofile.php3?k=1513835534&u=912'
        ]

    def parse(self, response):
        ''''''

        # Get parameters k and u in url
        o = urlparse(response.url)
        ids = parse_qs(o.query)

        # Load data through an item loader

        l = ProductLoader(item=Review(), response=response)
        l.add_value('k_id', ids['k'].pop() )
        l.add_value('u_id', ids['u'].pop() )

        # Div containing review portfolio
        portfolio = '//div[@class="portfolioContainer"]/'

        # About student
        summary_xpath = portfolio
        l.add_xpath('gender', summary_xpath+'div[2]/span/text()' )
        l.add_xpath('intelligence', summary_xpath+'div[3]/span/text()' )
        l.add_xpath('summary', summary_xpath+'div[5]/text()' )

        # Ratings provided by a student
        ratings_xpath = portfolio + 'div[1]/table/'
        l.add_xpath('educational_quality', ratings_xpath+'tr[1]/td[2]/font/text()' )
        l.add_xpath('faculty_accessibility', ratings_xpath+'tr[2]/td[4]/font/text()' )
        l.add_xpath('useful_schoolwork', ratings_xpath+'tr[2]/td[2]/font/text()' )
        l.add_xpath('excess_competition', ratings_xpath+'tr[3]/td[4]/font/text()' )
        l.add_xpath('academic_success', ratings_xpath+'tr[3]/td[2]/font/text()' )
        l.add_xpath('creativity_innovation', ratings_xpath+'tr[3]/td[4]/font/text()' )
        l.add_xpath('individual_value', ratings_xpath+'tr[4]/td[2]/font/text()' )
        l.add_xpath('university_resource_use', ratings_xpath+'tr[4]/td[4]/font/text()' )
        l.add_xpath('campus_aesthetics', ratings_xpath+'tr[5]/td[2]/font/text()' )
        l.add_xpath('friendliness', ratings_xpath+'tr[5]/td[4]/font/text()' )
        l.add_xpath('campus_maintenance', ratings_xpath+'tr[6]/td[2]/font/text()' )
        l.add_xpath('social_life', ratings_xpath+'tr[6]/td[4]/font/text()' )

        l.add_xpath('surrounding_city', ratings_xpath+'tr[7]/td[2]/font/text()' )
        l.add_xpath('extra_curriculars', ratings_xpath+'tr[7]/td[4]/font/text()' )
        l.add_xpath('safety', ratings_xpath+'tr[8]/td[2]/font/text()' )

        l.add_xpath('lowest_rated_cat', summary_xpath+'div[4]/table/tr[1]/td[1]/text()' )
        l.add_xpath('lowest_rating_val', summary_xpath+'div[4]/table/tr[1]/td[2]/b/text()' )
        l.add_xpath('highest_rated_cat', summary_xpath+'div[4]/table/tr[3]/td[1]/text()' )
        l.add_xpath('highest_rating_val', summary_xpath+'div[4]/table/tr[3]/td[2]/b/text()' )

        # Descriptions provided by student about college
        l.add_xpath('descr_student_body', ratings_xpath+'tr[10]/td/font[1]/font/text()' )
        l.add_xpath('descr_faculty', ratings_xpath+'tr[10]/td/font[2]/font/text()' )

        # Main comment and attributes
        l.add_xpath('date', summary_xpath+'div[6]/text()[1]' )
        l.add_xpath('major', summary_xpath+'div[6]/font[1]/b/text()' )

         # See: http://dh.newtfire.org/explainXPath.html on how to extract siblings after specified element
        l.add_xpath('review', summary_xpath+'div[6]/br[2]/following-sibling::text()' )

        return l.load_item()
