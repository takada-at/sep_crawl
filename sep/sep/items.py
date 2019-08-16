# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class EntryItem(Item):
    title = Field()
    link = Field()
    content = Field()


class Html(Item):
    content = Field()
    filepath = Field()
    link = link


class Text(Item):
    filepath = Field()
