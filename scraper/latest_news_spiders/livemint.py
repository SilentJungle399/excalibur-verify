import scrapy


class Livemint(scrapy.Spider):
    name = "livemint_latest"
    start_urls = [
        "https://www.livemint.com/latest-news",
    ]

    def parse(self, response: scrapy.http.Response):
        for article in response.css("div.listingNew"):
            article_url = article.xpath("@data-weburl").get()
            yield response.follow(
                article_url,
                callback = self.parse_article
            )

    def parse_article(self, response: scrapy.http.Response):
        yield {
            "title": response.css("h1.headline::text").get(),
            "content": "\n".join(response.css("div#mainArea p::text").getall()),
            "url": response.url,
            "source": "livemint"
        }
