# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GazetaDoPovoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    titulo = scrapy.Field(serialize=str)
    link = scrapy.Field(serialize=str)
    descricao_noticia = scrapy.Field(serialize=str)
    data_publicacao = scrapy.Field(serialize=str)
    data_extracao = scrapy.Field(serialize=str)
