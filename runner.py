from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tree_nation.spiders.tree_projects import TreeProjectsSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(TreeProjectsSpider)
process.start()
