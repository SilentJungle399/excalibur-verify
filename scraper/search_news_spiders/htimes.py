import scrapy
import requests


class HindustanTimes(scrapy.Spider):
    name = "htimes_search"
    search_query: str  # This is a type hint to suppress warnings in the IDE
    start_urls = [
        "https://www.hindustantimes.com/latest-news",
    ]

    def parse(self, response: scrapy.http.Response):
        req = requests.post("https://api.hindustantimes.com/api/articles/search", json = {
            "page": "1",
            "searchKeyword": self.search_query,
            "size": "30",
            "type": "story"
        })

        data = req.json()

        for result in data["content"]:
            yield scrapy.Request(
                result["metadata"]["canonicalUrl"],
                callback = self.parse_article
            )

    def parse_article(self, response: scrapy.http.Response):
        yield {
            "title": response.css("div.fullStory h1::text").get(),
            "content": "\n".join(response.css("div.storyDetails p::text").getall()),
            "url": response.url,
            "source": "htimes"
        }
