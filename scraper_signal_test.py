from scraper.search_news_spiders.htimes import HindustanTimes
from scraper.search_news_spiders.livemint import Livemint
from scraper.search_news_spiders.ndtv import NDTV
from scraper.search_news_spiders.thehindu import TheHindu

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(settings=get_project_settings())

process.crawl(HindustanTimes)
process.crawl(Livemint)
process.crawl(NDTV)
process.crawl(TheHindu)

process.start()
