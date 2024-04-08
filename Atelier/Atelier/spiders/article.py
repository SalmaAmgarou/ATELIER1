import scrapy


class ArticleSpider(scrapy.Spider):
    name = "article"
    allowed_domains = ["althawrah.ye"]
    start_urls = ["https://althawrah.ye/archives/category/%d8%a7%d9%84%d8%a7%d9%82%d8%aa%d8%b5%d8%a7%d8%af"]

    def parse(self, response):
        pass
