import multiprocessing
import os

from aiohttp import web

from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

app = web.Application()
router = web.RouteTableDef()


def run_crawler(query):
    process = CrawlerProcess(settings = get_project_settings())

    data = []

    def scrape_finished(item):
        data.append(item)

    for spider in os.listdir("scraper/search_news_spiders"):
        if not spider.startswith("__"):
            process.crawl(spider.strip(".py") + "_search", search_query = query)

    for crawler in process.crawlers:
        crawler.signals.connect(
            scrape_finished,
            signal = signals.item_scraped
        )

    process.start()

    return data


def search_news(query):
    with multiprocessing.Pool() as pool:
        data = pool.map(run_crawler, [query])
        return data


@router.post('/image')
async def index(request):
    print(request)
    # recognize news from image
    return web.Response(text = "Hello, world")


@router.post('/text')
async def index(request):
    text = (await request.json())['text']
    news_res = search_news(text)

    return web.Response(text = "Hello, world")


app.add_routes(router)
web.run_app(app)
