# scraping_studentsreviews
Scraping student reviews of universities from http://www.studentsreview.com

## Method

First, a list of universities and colleges will be scraped from links on three different pages:
* [http://www.studentsreview.com/college-search/lists-of-colleges-in-state.php3](http://www.studentsreview.com/college-search/lists-of-colleges-in-state.php3)
* [http://www.studentsreview.com/college-search/lists-of-colleges-in-city.php3](http://www.studentsreview.com/college-search/lists-of-colleges-in-city.php3)
* [http://www.studentsreview.com/AL/](http://www.studentsreview.com/AL/)

The first two pages contain links to search results of schools with different search terms.

The third page is a list of universities in Alabama (AL) but it also contains a navigation bar with links to pages containing a list of universities in other states and some countries (ex. Canada, UK, China). We use the navigation bar to scrape the list of universities beyond those in Alabama.

We create two scrapers. One called [via_search.py](scraping_studentsreviews/spiders/via_search.py) which extracts a link to each school's information page via the first two pages (above). The second scraper ([via_listing.py](scraping_studentsreviews/spiders/via_listing.py)) also scrapes links but through the third page (above).

To run the scraper to obtain the links via search, run.
```
cd path/to/repository/
scrapy crawl via_search -o 'data/schools_via_search_categories.csv'
```


Once a list of institutions has been created, we remove duplicates and go the comments page of each university and scrape the comments.



## Resources

* [Scrapy](https://doc.scrapy.org/en/latest/index.html)
* A gentle reminder about working with relative xpaths: After obtaining a set of elements using xpath, we can then extract another set of elements inside those elements but a `.` must be prefixed, esp. if the leading relative xpath starts with a `/`. [link](https://doc.scrapy.org/en/latest/topics/selectors.html#working-with-relative-xpaths)
