import scrapy
from pymongo import MongoClient

from ..items import AtelierItem


class ArticleSpider(scrapy.Spider):
    name = "article"
    allowed_domains = ["althawrah.ye"]
    start_urls = ["https://althawrah.ye/archives/category/%d8%a7%d9%84%d8%a7%d9%82%d8%aa%d8%b5%d8%a7%d8%af"]
    pages_visited = 0 # Initialize a counter to track pages visited
    def parse(self, response):
        articles = response.css("article.type-post")
        for article in articles:
            #extracting relative url for each post
            article_url = article.css('h2.title a.post-url::attr(href)').get()
            yield response.follow(article_url, callback=self.parse_article_page)
            # # Extracting title from each article
            # title = article.css("h2.title a.post-url").attrib["href"]
            # print(title)
        # Increment the pages visited
        self.pages_visited += 1

        # Stop the spider if the limit of 50 pages is reached
        if self.pages_visited >= 50:
            self.log("Reached the limit of 50 pages. Stopping the spider.")
            return

        next_page = response.css("div.pagination a.next::attr(href)").get() #returns link of next_page
        if next_page is not None:
            next_page_url = next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_article_page(self, response):


        content_paragraphs = response.css('div.single-post-content p::text').getall()
        item = AtelierItem()

        item['url'] = response.url
        item['title'] = response.css("h1.single-post-title span.post-title::text").get()
        item['pub_date'] = response.css("span.time time.post-published b::text").get()
        item['category'] = response.css("div.term-badges span.term-10893 a::text").get()
        item['content'] = ' '.join(content_paragraph.strip() for content_paragraph in content_paragraphs)

        yield item




            # response.css("article.type-post h2.title a").attrib)["href"]
        #articles.css("article.type-post h2.title a::text").g
