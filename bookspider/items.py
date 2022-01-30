# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookItem(scrapy.Item):
    novel_name = scrapy.Field()  # 对应book表的title
    novel_cover = scrapy.Field()  # 对应book表的cover，这里保存图片的url
    novel_author = scrapy.Field()  # 对应book表的author
    last_update = scrapy.Field()  # 对应book表的最后更新时间
    last_chapter = scrapy.Field()  # 对应book表的最后章节
    intro = scrapy.Field()  # 对应book表的intro
    topic = scrapy.Field()  # 对应book表的topic

class ChapterItem(scrapy.Item):
    book_title = scrapy.Field()
    chapter_title = scrapy.Field()   # 对应chapter表的chapter_title
    content = scrapy.Field()        # 对应chapter表的content，章节内容
    chapter_num = scrapy.Field()    # 章节号

class ModuleItem(scrapy.Item):
    module_name = scrapy.Field()  # 对应module表的module_name，书籍所属模块名
