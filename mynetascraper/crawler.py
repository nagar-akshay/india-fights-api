from scrapy.crawler import CrawlerProcess

from mynetascraper.spiders.constituencyscraper import ConstituencyscraperSpider
from mynetascraper.spiders.netascraper import NetascraperSpider

# Run Scrapy programmatically
process = CrawlerProcess(settings={
    'FEEDS': {
        'scraper.json': {'format': 'json'},
    },
})

process.crawl(ConstituencyscraperSpider)
process.start()  # This will block until the crawl is finished
