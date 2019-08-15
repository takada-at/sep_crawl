# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from bs4 import BeautifulSoup
from sep.items import Html, Text
from sep.path import url2path, textpath, entries_text
from scrapy.selector import Selector

import re


class SavePipeline:
    def process_item(self, item, spider):
        fpath = url2path(item['link'])
        with fpath.open('w') as wio:
            content = item['content']
            wio.write(content)
        return Html(filepath=fpath, content=content)


class Convert2Text:
    def process_item(self, item, spider):
        paragraphs = convert(item['content'])
        path = textpath(item['filepath'])
        # with path.open('w') as wio:
        #  wio.write("\n".join(paragraphs))
        with entries_text().open('a') as wio:
            wio.write('\n'.join(paragraphs) + "\n")
        return item


def convert(html):
    selector = Selector(text=html)
    article = selector.css('#article')
    articlestr = article.extract()[0]
    bib = article.xpath('//h2[starts-with(., "Bibliography")]').extract()[0]
    articlebody = articlestr.split(bib)[0]
    sel = Selector(text=articlebody)
    paragraphs = []
    noise = ['"', '(', ')', '[', ']', ',', '(', ')', '.', "'", ":", ";", "\n", "—", "?", "!", "“", "”", "-"]
    for p in sel.xpath('(//p|//blockquote|//h1|//h2|//h3)'):
        string = BeautifulSoup(p.extract(), features="lxml").get_text()
        tokens = tokenizer(string.lower())
        paragraphs.append(" ".join(tokens))
    return paragraphs


token_pattern = r"(?u)\b\w\w+\b"
token_reg = re.compile(token_pattern)

def tokenizer(doc):
    return token_reg.findall(doc)
