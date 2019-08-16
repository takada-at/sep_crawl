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
import spacy


nlp = spacy.load("en_core_web_sm")


class SavePipeline:
    def process_item(self, item, spider):
        fpath = url2path(item['link'])
        with fpath.open('w') as wio:
            content = item['content']
            wio.write(content)
        return Html(filepath=fpath, content=content,
                    link=item['link'])


class Convert2Text:
    def process_item(self, item, spider):
        convert_and_save(item)
        return item


def convert_and_save(item):
    paragraphs = convert(item['content'])
    path = textpath(item['link'])
    with path.open('w') as wio:
      wio.write("\n".join(paragraphs) + "\n")


def convert(html):
    selector = Selector(text=html)
    article = selector.css('#article')
    articlestr = article.extract()[0]
    bib = article.xpath('//h2[starts-with(., "Bibliography")]').extract()[0]
    articlebody = articlestr.split(bib)[0]
    sel = Selector(text=articlebody)
    text = BeautifulSoup(sel.extract(), features="lxml").get_text()
    tokens = nlp(text)
    result = []
    ignores = {',', '.', ':', ';', '(', ')', '“', '“', '”', '"', "'", "-", "—", "[", "]", "!", "?", "{", "}", "’", "‘"}
    paragraphs = []
    for p in sel.xpath('(//p|//blockquote)'):
        string = BeautifulSoup(p.extract(), features="lxml").get_text()
        string = string.replace('\n', ' ').lower().strip()
        if not string:
            continue
        paragraphs.append(string)
    tokens = nlp("\n".join(paragraphs))
    for sent in tokens.sents:
        stokens = [t.text for t in sent]
        stokens = [t for t in stokens if t not in ignores and t]
        if not stokens:
            continue
        s = " ".join(stokens).strip()
        for i in ignores:
            s = s.replace(i, "")
        if not s:
            continue
        result.append(s)
    return result


token_pattern = r"(?u)\b\w\w+\b"
token_reg = re.compile(token_pattern)


def tokenizer(doc):
    return token_reg.findall(doc)
