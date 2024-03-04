import scrapy


class NDTV(scrapy.Spider):
    name = "ndtv_search"
    search_query: str  # This is a type hint to suppress warnings in the IDE

    def start_requests(self):
        yield scrapy.Request(
            url = f"https://www.ndtv.com/search?searchtext={self.search_query}",
            callback = self.parse
        )

    def parse(self, response: scrapy.http.Response):
        for article in response.css("div.src_itm-ttl a"):
            article_url = article.xpath("@href").get()
            yield response.follow(
                article_url,
                callback = self.parse_sports_article if article_url.startswith("https://sports.ndtv.com/") else self.parse_ndtv_article
            )

    def parse_ndtv_article(self, response: scrapy.http.Response):
        yield {
            "title": response.xpath("//h1[@itemprop='headline']/text()").get(),
            "content": "\n".join(response.css("div#ins_storybody p::text").getall()),
            "url": response.url,
            "source": "ndtv"
        }

    def parse_sports_article(self, response: scrapy.http.Response):
        article_div = response.css("div#print-1")
        yield {
            "title": article_div.css("h1::text").get(),
            "content": "\n".join(response.css("div.story__content p::text").getall()),
            "url": response.url,
            "source": "ndtv"
        }
