import scrapy


class HindustanTimes(scrapy.Spider):
    name = "htimes_latest"
    start_urls = [
        "https://www.hindustantimes.com/latest-news",
    ]

    def parse(self, response: scrapy.http.Response):
        for article in response.css("div.articleClick"):
            article_url = article.xpath("@data-weburl").get()
            yield response.follow(
                article_url,
                callback = self.parse_article
            )

    def parse_article(self, response: scrapy.http.Response):
        yield {
            "title": response.css("div.fullStory h1::text").get(),
            "content": "\n".join(response.css("div.storyDetails p::text").getall()),
            "url": response.url,
        }
