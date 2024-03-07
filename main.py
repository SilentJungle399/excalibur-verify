import multiprocessing
import json
import os

from aiohttp import web

from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.gnews import GNews

from sentence_transformers import SentenceTransformer, util
import re
from transformers import pipeline

app = web.Application()
router = web.RouteTableDef()


def eng_verify(_news):
    return (len(re.findall(r'[a-zA-Z]', _news)) / len(_news)) > 0.75


def run_crawler(query):
    process = CrawlerProcess(settings = get_project_settings())

    data = []

    def scrape_finished(item):
        data.append(item)

    process.crawl(GNews, search_query = query)

    for crawler in process.crawlers:
        crawler.signals.connect(
            scrape_finished,
            signal = signals.item_scraped
        )

    process.start()

    return data


def search_news(query):
    with multiprocessing.Pool() as pool:
        data = pool.map(run_crawler, [query, ])
        # fake_data = pool.map(run_crawler, [query + " is fake claim", ])
        calculated = pool.map(calculate_query, [(data[0], query), ])
        # calculated = calculate_query(data[0], fake_data[0], query)

        return calculated


def calculate_query(args):
    print(args)
    summarizer = pipeline("summarization", model = "facebook/bart-large-cnn")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    def fmt_news(_news):
        # first layer filter
        _news = _news.replace("\n", " ")
        _news = re.sub(' +', ' ', _news).strip()

        # summarize
        _news = summarizer(_news[:2048], max_length = 256, min_length = 50, do_sample = False)[0]["summary_text"]

        return _news

    news_res, data = args
    fmt_content = [fmt_news(n["content"]) for n in news_res if len(n["content"]) > 1000 and eng_verify(n["content"])]
    print("Content formatted")

    query_embedding = model.encode(data)

    passage_embedding = model.encode(fmt_content)

    print("Embeddings calculated")

    sim = []

    for passage in passage_embedding:
        sim.append(util.cos_sim(query_embedding, passage))

    print("Normal", sum(sim) / len(sim))
    return float(sum(sim) / len(sim)), news_res


@router.post('/api/text')
async def index(request):
    text = (await request.json())['text']
    print("search request received ", text)

    res = search_news(text)

    return web.Response(text = json.dumps(res))


@router.get('/')
async def index(request):
    return web.FileResponse('public/front.html')


local_dir = os.path.join(os.path.dirname(__file__), "public")
app.router.add_static('/public', local_dir)

app.add_routes(router)
web.run_app(app)
