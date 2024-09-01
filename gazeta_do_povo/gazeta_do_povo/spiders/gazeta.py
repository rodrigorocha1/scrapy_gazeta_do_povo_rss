import scrapy
import scrapy.spiders
from scrapy.http import Response
from gazeta_do_povo.items import GazetaDoPovoItem
from datetime import datetime


class GazetaSpider(scrapy.spiders.XMLFeedSpider):
    name = "gazeta"
    allowed_domains = ["www.gazetadopovo.com.br"]
    start_urls = ["https://www.gazetadopovo.com.br/feed/rss/mundo.xml"]
    itertag = 'item'

    def parse_node(self, response: Response, node: scrapy.Selector):
        titulo = node.xpath('title/text()').get()
        link = node.xpath('link/text()').get()
        descricao_noticia = node.xpath('description/text()').get()
        data_publicacao = node.xpath('pubDate/text()').get()
        item = GazetaDoPovoItem()
        item['titulo'] = titulo
        item['link'] = link
        item['descricao_noticia'] = descricao_noticia
        item['data_publicacao'] = data_publicacao
        item['data_extracao'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        yield item
