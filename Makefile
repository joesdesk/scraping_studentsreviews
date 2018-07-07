all: comment_pages.csv

# Create lists of college URLs
via_listing.csv:
	scrapy crawl via_listing -o 'via_listing.csv'

via_search.csv:
	scrapy crawl via_search -o 'via_search.csv'

# Create lists of full review URLs
comment_pages.csv: via_listing.csv via_search.csv
	scrapy crawl comment_pages -o 'comment_pages.csv'
