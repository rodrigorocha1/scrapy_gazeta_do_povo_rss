# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from datetime import datetime
from scrapy.crawler import Crawler
from scrapy.spiders import Spider
import sqlite3
from gazeta_do_povo.items import GazetaDoPovoItem
import os


class CleanGazetaDoPovoPipeline:
    def process_item(self, item, spider):

        item['descricao_noticia'] = item['descricao_noticia'].replace(
            "]]>", "").replace("<![CDATA[", "")
        text_pattern = re.compile(r'<br\s*/>\s*(.*)')
        item['descricao_noticia'] = text_pattern.search(
            item['descricao_noticia'])
        if item['descricao_noticia']:
            item['descricao_noticia'] = item['descricao_noticia'].group(1)
        item['data_publicacao'] = item['data_publicacao']
        item['data_publicacao'] = datetime.strptime(
            item['data_publicacao'], "%a, %d %b %Y %H:%M:%S %Z")

        item['data_publicacao'] = item['data_publicacao'].strftime(
            " %d-%m-%Y %H:%M:%S")

        return item


class SqlitePipeline:
    tabela = "NOTICIAS"

    def __init__(self, sqlite_db: str) -> None:
        self.sqlite_db = sqlite_db

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "SqlitePipeline":
        return cls(
            sqlite_db=crawler.settings.get(
                'SQLITE_DATABASE')
        )

    def open_spider(self, spider: Spider):
        self.conn = sqlite3.connect(self.sqlite_db)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider: Spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item: GazetaDoPovoItem, spider: Spider):
        item_dic = ItemAdapter(item).asdict()
        values = list(item_dic.values())
        marcadores_de_posicao = ', '.join('?' * len(values))
        sql = f'''
            INSERT INTO {self.tabela} (titulo, link, descricao_noticia, data_publicacao, data_extracao)
            VALUES ({marcadores_de_posicao})
        '''
        spider.logger.info(f'Executando consulta SQL: {sql}')
        spider.logger.info(f'Valores: {values}')
        self.cursor.execute(sql, values)
        return item
