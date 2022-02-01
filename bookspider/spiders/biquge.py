# -*- coding: utf-8 -*-

import scrapy
from bookspider.items import BookItem,ChapterItem,ModuleItem

domain = "https://www.xbiquge.la"

class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    # allowed_domains = ['xxx.com']
    start_urls = ['https://www.xbiquge.la/14/14718/']

    def parse(self, response, **kwargs):
        topics = response.xpath("//div[@class='nav']/ul/li/a")  # 爬取每个a标签
        topics = topics[2:8]

        for topic in topics:
            topic_name = topic.xpath("./text()").extract()[0]
            item = ModuleItem()
            item['module_name'] = topic_name
            yield item

        url = "https://www.xbiquge.la/xiaoshuodaquan/"
        yield scrapy.Request(url,callback=self.start)

    def start(self, response):
        books  = response.xpath("//div[@class='novellist']/ul/li/a")
        for book in books:
            book_url = book.xpath("./@href").extract()[0]
            yield scrapy.Request(book_url, callback=self.getBook)

    def getBook(self, response):
        topic_name = response.xpath("//div[@class='con_top']/a/text()")[1].extract()
        cover_url = response.xpath("//div[@id='fmimg']/img/@src").extract()[0]
        book_name = response.xpath("//div[@id='info']/h1/text()").extract()[0]
        authors = response.xpath("//div[@id='info']/p[1]/text()").extract()[0].split("：")[1]
        author = "佚名"
        if authors:
            author = authors
        last_update_times = response.xpath("//div[@id='info']/p[3]/text()").extract()[0]
        last_update_time = ""
        if len(last_update_times) > 5:
            last_update_time = last_update_times[5:]
        last_update_chapter = response.xpath("//div[@id='info']/p[4]/a/text()").extract()[0]
        intros = response.xpath("//div[@id='intro']/p[2]/text()")
        intro = "暂无简介"
        if len(intros):
            intro = intros.extract()[0]
            intro = self.handleIntro(intro)

        item = BookItem()
        item['novel_name'] = book_name
        item['novel_cover'] = cover_url
        item['novel_author'] = author
        item['last_update'] = last_update_time
        item['last_chapter'] = last_update_chapter
        item['intro'] = intro
        item['topic'] = topic_name
        yield item

        chapters = response.xpath("//div[@id='list']/dl/dd/a")
        number = 0
        for chapter in chapters:
            chapter_url = chapter.xpath("./@href").extract()[0]
            chapter_name = chapter.xpath("./text()").extract()[0]
            number += 1
            chapter_url = domain + chapter_url
            yield scrapy.Request(chapter_url, meta={"book_name": book_name,
                                                    "chapter_name": chapter_name,
                                                    "chapter_num": number}, callback=self.getContent)

    def getContent(self, response):
        book_name = response.meta["book_name"]
        chapter_name = response.meta["chapter_name"]
        chapter_num = response.meta["chapter_num"]
        contents = response.xpath("//div[@id='content']/text()").extract()
        content = ""
        for con in contents:
            if con != '\r':
                con = self.handleContent(con)
                content += con
                content += '\n'
        content = content.strip()    # 去文本末尾换行符

        item = ChapterItem()
        item["book_title"] = book_name
        item["chapter_title"] = chapter_name
        item["chapter_num"] = chapter_num
        item["content"] = content
        yield item

    def handleIntro(self, intro):
        intro = intro.replace("\u3000", '') # 去掉三种空格
        intro = intro.replace("\u00A0", '')
        intro = intro.replace("\u0020", '')
        intro = intro.replace("javascript:share({content:'", '')
        intro = intro.replace(' ', '')
        intro = intro.replace('\r', '')
        intro = intro.replace('\n', '')
        return intro

    def handleContent(self, content):
        content = content.replace('\xa0', '')  # 去空格(\xa0)
        content = content.replace("\u3000", '')  # 去掉三种空格
        content = content.replace("\u00A0", '')
        content = content.replace("\u0020", '')
        content = content.replace("?", '')      # 去英文?符
        content = content.replace("\r", '')    # 去掉转义符\r
        content = content.replace("\"", "")
        content = content.replace(" ", '')  # 去空格
        return content
