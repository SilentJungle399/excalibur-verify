import scrapy

# TODO: DYNAMIC CONTENT - NEEDS PLAYWRIGHT (BROWSER AUTOMATION) TO WORK

class TheHindu(scrapy.Spider):
    name = "thehindu_search"
    search_query: str  # This is a type hint to suppress warnings in the IDE

    def start_requests(self):
        yield scrapy.Request(
            url = f"https://www.thehindu.com/search/#gsc.tab=0&gsc.q={self.search_query}",
            callback = self.parse
        )

    def parse(self, response: scrapy.http.Response):
        for article in response.css("a.gs-title"):
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
            "source": "thehindu"
        }
