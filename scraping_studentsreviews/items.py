# Models for scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, TakeFirst, Join

class Review(scrapy.Item):
    '''Container for the review and associated data.
    '''

    # Parameters k and u in the url of review
    k_id = scrapy.Field()
    u_id = scrapy.Field()

    # University name
    university = scrapy.Field()

    # Student profile
    gender = scrapy.Field()
    intelligence = scrapy.Field()
    summary = scrapy.Field()

    lowest_rated_cat = scrapy.Field()
    lowest_rating_val = scrapy.Field()
    highest_rated_cat = scrapy.Field()
    highest_rating_val = scrapy.Field()

    # Student's ratings
    educational_quality = scrapy.Field()
    faculty_accessibility = scrapy.Field()

    useful_schoolwork = scrapy.Field()
    excess_competition = scrapy.Field()

    academic_success = scrapy.Field()
    creativity_innovation = scrapy.Field()

    individual_value = scrapy.Field()
    university_resource_use = scrapy.Field()

    campus_aesthetics = scrapy.Field()
    friendliness = scrapy.Field()

    campus_maintenance = scrapy.Field()
    social_life = scrapy.Field()

    surrounding_city = scrapy.Field()
    extra_curriculars = scrapy.Field()

    safety = scrapy.Field()
    
    # Descriptions provided by student about college
    descr_student_body = scrapy.Field()
    descr_faculty = scrapy.Field()

    # Main comment and attributes
    date = scrapy.Field()
    major = scrapy.Field()
    review = scrapy.Field()

    pass


class ProductLoader(ItemLoader):
    '''Adds a processor for the review field in item which turns a review into a string.
    '''
    default_output_processor = TakeFirst()

    review_in = Identity()
    review_in = Join(separator=u'\n')
