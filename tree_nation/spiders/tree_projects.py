import scrapy
from scrapy_splash import SplashRequest
from logzero import logger


class TreeProjectsSpider(scrapy.Spider):
    name = 'tree_projects'
    allowed_domains = ['tree-nation.com']
    script = '''
        function main(splash, args)
            url = args.url
            splash.images_enabled = false
            assert(splash:go(url))
            assert(splash:wait(0.5))
            while true do
              button = splash:select('a.btn.btn-more')
              if not button then break end
              button:mouse_click()
              splash:wait(2)
            end
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.tree-nation.com/projects", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })

    def parse(self, response):
        projects = response.xpath("//div[@class='project-prev1__content']/h3/a/@href").getall()
        logger.info(f"FOUND {len(projects)} PROJECTS")
        for project in projects:
            project = project[:-7] + "about"
            yield SplashRequest(url=project, callback=self.parse_project, args={'wait': 2,
                                                                                'images_enabled': False})

    def parse_project(self, response):
        logger.info(f"SCRAPING {response.url}")
        trees_planted, co2_saved, _ = response.xpath(
            "//span[contains(@class, 'pr-header__stat-value')]/text()").getall()
        yield {
            "title": " ".join(response.xpath("//div[@class='meta']/h2/text()").getall()),
            "description": response.xpath("//div[@class='description']/p/text()").get(),
            "trees_planted": trees_planted,
            "co2_saved": co2_saved,
            "tags": ",".join(response.xpath("//h4[@class='impact-box__title']/text()").getall())
        }
