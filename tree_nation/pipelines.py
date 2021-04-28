# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from logzero import logger
import sqlite3


class TreeNationPipeline:

    def open_spider(self, spider):
        logger.warn("SPIDER OPENED FROM PIPELINE")
        self.connection = sqlite3.connect("tree.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
            CREATE TABLE tree_projects
            (
                title         TEXT,
                description   TEXT,
                trees_planted TEXT,
                co2_saved     TEXT,
                tags          TEXT
            )  
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        logger.warn("SPIDER CLOSED FROM PIPELINE")
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO tree_projects (title,description,trees_planted,co2_saved,tags) VALUES(?,?,?,?,?)

        ''', (
            item.get('title'),
            item.get('description'),
            item.get('trees_planted'),
            item.get('co2_saved'),
            item.get('tags'),
        ))
        self.connection.commit()
        return item
