import json

import scrapy
import requests


class Livemint(scrapy.Spider):
    name = "livemint_search"
    search_query: str  # This is a type hint to suppress warnings in the IDE

    def start_requests(self):
        yield scrapy.FormRequest(
            url="https://www.livemint.com/search",
            callback=self.parse,
            formdata = {
                "searchKeyword": self.search_query,
            },
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )

    def parse(self, response: scrapy.http.Response):
        for article in response.css("h2.headline a"):
            article_url = article.xpath("@href").get()
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
