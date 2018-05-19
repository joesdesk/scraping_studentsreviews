# Models for scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Review(scrapy.Item):
    ''''''

    # Parameters k and u in the url of review
    k_id = scrapy.Field()
    u_id = scrapy.Field()

    # About university
    university = scrapy.Field()

    # About student
    gender = scrapy.Field()
    intelligence = scrapy.Field()
    summary = scrapy.Field()

    # Ratings provided by a student
    educational_quality = scrapy.Field()
    useful_schoolwork = scrapy.Field()
    academic_success = scrapy.Field()
    individual_value = scrapy.Field()
    campus_aesthetics = scrapy.Field()
    campus_maintenance = scrapy.Field()
    surrounding_city = scrapy.Field()
    safety = scrapy.Field()
    faculty_accessibility = scrapy.Field()
    excess_competition = scrapy.Field()
    creativity_innovation = scrapy.Field()
    university_resource_use = scrapy.Field()
    friendliness = scrapy.Field()
    social_life = scrapy.Field()
    extra_curriculars = scrapy.Field()

    lowest_rated_cat = scrapy.Field()
    lowest_rating_val = scrapy.Field()
    highest_rated_cat = scrapy.Field()
    highest_rating_val = scrapy.Field()

    # Descriptions provided by student about college
    descr_student_body = scrapy.Field()
    descr_faculty = scrapy.Field()

    # Main comment and attributes
    date = scrapy.Field()
    major = scrapy.Field()
    review = scrapy.Field()

    pass
