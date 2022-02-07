# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter
from twisted.enterprise import adbapi
import datetime
from bookspider.items import BookItem,ModuleItem,ChapterItem

class biqugeSpiderPipeline:
    def __init__(self):
        self.connect = pymysql.connect(host='localhost',
                                       user='root',
                                       password='159753',
                                       db='web_novel',
                                       port=3306,
                                       charset="utf8mb4")
        self.cursor = self.connect.cursor()

    def process_item(self,item,spider):
        if type(item) == ModuleItem:
            sql = """INSERT INTO module(module_name) VALUES("%s")""" % (item["module_name"])
            self.cursor.execute(sql)
            self.connect.commit()

        elif type(item) == BookItem:
            novel_name = item["novel_name"]
            novel_cover = item["novel_cover"]
            novel_author = item["novel_author"]
            last_update = item["last_update"]
            last_chapter = item["last_chapter"]
            intro = item["intro"]
            topic = item["topic"]
            # 格式化时间
            format = '%Y-%m-%d %H:%M:%S'
            last_update = datetime.datetime.strptime(last_update, format)  # <class 'datetime.datetime'>
            last_update = last_update.strftime(format)   #datetime对象转化为字符串
            sql1 = """INSERT INTO book(novel_name,cover,author,last_update,last_chapter,intro,
                    topic) VALUES("%s","%s","%s","%s","%s","%s","%s")""" \
                   % (novel_name,novel_cover,novel_author,last_update,last_chapter,intro,topic)
            self.cursor.execute(sql1)
            self.connect.commit()

        elif type(item) == ChapterItem:
            novel_id = item["novel_id"]
            chapter_title = item["chapter_title"]
            content = item["content"]
            chapter_num = item["chapter_num"]
            sql = """INSERT INTO chapter(novel_id,chapter_title,content,chapter_num)
            VALUES("%s","%s","%s","%s")""" %(novel_id,chapter_title,content,chapter_num)
            self.connect.ping(reconnect=True)
            self.cursor.execute(sql)
            self.connect.commit()
        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()
