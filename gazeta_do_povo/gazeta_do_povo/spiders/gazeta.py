import scrapy
import scrapy.spiders
from scrapy.http import Response
from gazeta_do_povo.items import GazetaDoPovoItem


class GazetaSpider(scrapy.spiders.XMLFeedSpider):
    name = "gazeta"
    allowed_domains = ["www.gazetadopovo.com.br"]
    start_urls = ["https://www.gazetadopovo.com.br/feed/rss/mundo.xml"]
    itertag = 'item'

    def parse_node(self, response: Response, node: scrapy.Selector):
        titulo = node.xpath('title/text()').get()
        link = node.xpath('link/text()').get()
        descricao_noticia = node.xpath('description/text()').get()
        item = GazetaDoPovoItem()
        item['titulo'] = titulo
        item['link'] = link
        item['descricao_noticia'] = descricao_noticia

        yield item
