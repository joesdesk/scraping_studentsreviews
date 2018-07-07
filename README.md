# scraping_studentsreviews
University students from across the world give comprehensive reviews of their universities at http://www.studentsreview.com. This project scrapes those reviews to obtain data for machine learning or natural language projects.

## Contents
* [Method](#Method)
* Computing via the cloud: Amazon EC2
* Resources

## Method

### Creating a list of institution pages
The first step of the scraper is to find links to every college webpage in the website.
First, a list of universities and colleges will be scraped from links on three different pages:
* [http://www.studentsreview.com/college-search/lists-of-colleges-in-state.php3](http://www.studentsreview.com/college-search/lists-of-colleges-in-state.php3)
* [http://www.studentsreview.com/college-search/lists-of-colleges-in-city.php3](http://www.studentsreview.com/college-search/lists-of-colleges-in-city.php3)
* [http://www.studentsreview.com/AL/](http://www.studentsreview.com/AL/)

The first two pages contain links to search results of schools with different search terms.

The third page is a list of universities in Alabama (AL). However, it also contains a navigation bar with links to pages containing a list of universities in other states and some countries (ex. Canada, UK, China). We use the navigation bar to scrape the list of universities beyond those in Alabama.

We create two scrapers. One called [via_search.py](scraping_studentsreviews/spiders/via_search.py) which extracts a link to each school's information page via the first two pages (above). The second scraper ([via_listing.py](scraping_studentsreviews/spiders/via_listing.py)) also scrapes links but through the third page (above).

To run the scraper to obtain the links, run
```
cd path/to/repository/
scrapy crawl via_search -o 'data/via_search.csv'
scrapy crawl via_listing -o 'data/via_listing.csv'
```

This creates two csv's in the data folder of the repository. The csv's only have one column which contain the links. The column has a header named `link`.


### Creating a list of full comment pages
Once a list of institutions has been created, we remove duplicates that might have resulted from our aggressive search for a list of colleges. We then have a list of URLs containing information about the institution. Oddly enough, some are aliases of each other. To remedy this, we follow the url on the page to itself so we get the 'official' URL. We then go through a second round of duplicate removal. The first page containing a summary of the comments can be obtained by making a tweak to the 'official' URL.

To run the scraper to obtain the links to the colleges.
```
scrapy crawl comment_pages -o 'data/comment_pages.csv'
```

This creates a the csv `comment_pages.csv` in the `data` directory containing the list of URLs for each institution.


## via the Cloud: Amazon EC2
Because of the number of pages to scrape, scraping the links may take several hours overnight if the internet connection is slow. The task can be performed much faster through the cloud. I used an Amazon EC2 instance to do this. Using the following procedure, it only took about 20 minutes to obtain the data.


## Resources

* [Scrapy](https://doc.scrapy.org/en/latest/index.html)
* A gentle reminder about working with relative xpaths: After obtaining a set of elements using xpath, we can then extract another set of elements inside those elements but a `.` must be prefixed, esp. if the leading relative xpath starts with a `/`. [link](https://doc.scrapy.org/en/latest/topics/selectors.html#working-with-relative-xpaths)
