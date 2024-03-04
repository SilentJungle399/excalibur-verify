import time

import multiprocessing

from scrapy import signals

from scraper.search_news_spiders.htimes import HindustanTimes
from scraper.search_news_spiders.livemint import Livemint
from scraper.search_news_spiders.ndtv import NDTV
from scraper.search_news_spiders.thehindu import TheHindu

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


spiders = [
    HindustanTimes,
    Livemint,
    NDTV,
    TheHindu,
]


def run_crawler(query):
    process = CrawlerProcess(settings = get_project_settings())

    data = []

    def scrape_finished(item):
        data.append(item)

    for spider in spiders:
        process.crawl(spider, search_query = query)

    for crawler in process.crawlers:
        crawler.signals.connect(
            scrape_finished,
            signal = signals.item_scraped
        )

    process.start()

    return data


def launch_crawler(query):
    t1 = time.time()
    with multiprocessing.Pool() as pool:
        data = pool.map(run_crawler, [query])
        print(len(data), data)

    print(time.time() - t1)


launch_crawler("covid")
print("waiting")
time.sleep(3)

launch_crawler("covid")
print("waiting")
time.sleep(3)

launch_crawler("covid")
print("waiting")
time.sleep(3)

