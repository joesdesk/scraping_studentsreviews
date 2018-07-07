all: comment_pages.csv

# Create lists of college URLs
data/via_listing.csv:
	scrapy crawl via_listing -o 'data/via_listing.csv'

data/via_search.csv:
	scrapy crawl via_search -o 'data/via_search.csv'

# Create lists of full review URLs
data/comment_pages.csv: data/via_listing.csv data/via_search.csv
	scrapy crawl comment_pages -o 'data/comment_pages.csv'
