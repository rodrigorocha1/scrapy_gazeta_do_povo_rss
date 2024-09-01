# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from datetime import datetime


class CleanGazetaDoPovoPipeline:
    def process_item(self, item, spider):

        item['descricao_noticia'] = item['descricao_noticia'].replace(
            "]]>", "").replace("<![CDATA[", "")
        text_pattern = re.compile(r'<br\s*/>\s*(.*)')
        item['descricao_noticia'] = text_pattern.search(
            item['descricao_noticia'])
        if item['descricao_noticia']:
            item['descricao_noticia'] = item['descricao_noticia'].group(1)

        item['data_publicacao'] = datetime.strptime(
            item['data_publicacao'], "%a, %d %b %Y %H:%M:%S %Z")

        item['data_publicacao'] = item['data_publicacao'].strftime(
            " %d-%m-%Y %H:%M:%S")

        return item


class SqlitePipeline:
    pass
