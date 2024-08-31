import scrapy


class GazetaSpider(scrapy.Spider):
    name = "gazeta"
    allowed_domains = ["www.gazetadopovo.com.br"]
    start_urls = ["https://www.gazetadopovo.com.br/feed/rss/mundo.xml"]

    def parse(self, response):
        pass
