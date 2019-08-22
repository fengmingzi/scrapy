import sys
from scrapy.utils.project import get_project_settings
from scrapyuniversal.spiders.universal import UniversalSpider
from scrapyuniversal.utils import get_config
from scrapy.crawler import CrawlerProcess

def run():
    # name = sys.argv[1] # json配置文件的名称
    name = 'china'
    custom_settings = get_config(name)
    spider = custom_settings.get('spider', 'universal')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    settings.update(custom_settings.get('settings'))
    process = CrawlerProcess(settings)
    process.crawl(spider, **{'name': name})# 第一个参数spider是要启动的爬虫类名，第二个参数：**{'name': name}是universal类中init初始化方法中name参数
    process.start()


if __name__ == '__main__':
    run()
