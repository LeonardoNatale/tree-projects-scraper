import scrapy
from scrapy_splash import SplashRequest


class TreeProjectsSpider(scrapy.Spider):
    name = 'tree_projects'
    allowed_domains = ['www.tree-nation.com']
    script = '''
        function main(splash, args)
            url = args.url
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
        for p in projects:
            print(p)

    def parse_project(self, response):
        pass