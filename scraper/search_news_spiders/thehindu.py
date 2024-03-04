import scrapy


class TheHindu(scrapy.Spider):
    name = "thehindu_search"
    start_urls = [
        "https://www.thehindu.com/latest-news",
    ]

    def parse(self, response: scrapy.http.Response):
        for article in response.css("h3.title a"):
            article_url = article.xpath("@href").get()
            yield response.follow(
                article_url,
                callback = self.parse_article
            )

    def parse_article(self, response: scrapy.http.Response):
        yield {
            "title": response.css("h1[itemprop='name']::text").get(),
            "content": "\n".join(response.css("div[itemprop='articleBody'] p::text").getall()),
            "url": response.url,
        }
