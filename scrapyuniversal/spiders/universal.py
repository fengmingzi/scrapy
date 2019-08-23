# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyuniversal.items import *
from scrapyuniversal.loaders import *
from scrapyuniversal.utils import get_config
from scrapyuniversal import urls
from scrapyuniversal.rules import SpiderRules
from scrapy_splash import SplashRequest
from scrapy.http import Request

class UniversalSpider(CrawlSpider):
    name = 'universal'
    
    def __init__(self, name, *args, **kwargs):
        # 获取自定义的json配置文件
        config = get_config(name)
        self.config = config


        # rules配置
        self.rules = SpiderRules(detailUrlXpaths='//div[@class="p-con"]/div[@class="p-box"]/ul[@class="products"]',
                                 detailTags=('a', 'area'),
                                 detailAttrs=('href',), detailCallback='parse_item', isSplash=True).rules.get(config.get('rules'))
        # self.rules = rules.get(config.get('rules'))

        # start_urls配置
        start_urls = config.get('start_urls')
        if start_urls:
            if start_urls.get('type') == 'static':
                self.start_urls = start_urls.get('value')
            elif start_urls.get('type') == 'dynamic':
                self.start_urls = list(eval('urls.' + start_urls.get('method'))(*start_urls.get('args', [])))

        # allowed_domains配置
        self.allowed_domains = config.get('allowed_domains')
        super(UniversalSpider, self).__init__(*args, **kwargs)

    # 重写start_requests,便于对start_urls进行处理
    def start_requests(self):
        for url in self.start_urls:
            print("进入首页")
            print(url)
            # splash:runjs("document.getElementsByClassName('laypage_next').click()")   "document.querySelector('#laypage_2 a.laypage_next').click()"
            lua_script = '''
                function main(splash)
                    splash.images_enabled = false
                    splash:go(splash.args.url)
                    splash:wait(2)
                    js = string.format("document.querySelector('.laypage_next').setAttribute('data-page',%d);document.querySelector('.laypage_next').click()", splash.args.page)
                    splash:runjs(js)
                    splash:wait(2)
                    return splash:html()
                end
            '''

            for page in range(1, 4):
                # yield Request(url)
                yield SplashRequest(url, callback=self.parse, endpoint='execute', args={'lua_source': lua_script, 'page': page})

    # 重写parse，处理start_url页面，为了实现翻页功能
    def parse1(self, response):

        # 拿到入口页的详情链接


        # 拿到下一页xpath，判断是否有下一页的属性

        #如果有下一页
        lua_script = '''
            function main(splash)
                splash:go(splash.args.url)
                splash:wait(2)
                splash:runjs("document.getElementsByClassName('laypage_next').click()")
                splash:wait(2)
                return splash:html()
            end
        '''

        # 拿到start_url列表页，然后不断点击
        yield SplashRequest(response.url, endpoint='execute', args={'lua_source': lua_script}, dont_filter=True)
        # 点击下一页按钮，
        # 根据start_url的response实现翻页，并加入request中
        # 获取翻页的xpath拿到url，或者根据事件实现翻页

    def parse_urls(self, response):
        # 调用_requests_to_follow方法，根据Rule规则获取所有的详情页
        self._requests_to_follow(response)  # 列表页response


    # 处理Rule中增加process_request参数为splash_request的Request请求
    def splash_request(self, request, response):
        """
        :param request: Request对象（是一个字典；怎么取值就不说了吧！！）
        :return: SplashRequest的请求
        """
        # dont_process_response=True 参数表示不更改响应对象类型（默认为：HTMLResponse；更改后为：SplashTextResponse）
        # args={'wait': 0.5} 表示传递等待参数0.5（Splash会渲染0.5s的时间）
        # meta 传递请求的当前请求的URL
        # TODO 这里需要根据定义的不同类型的lua操作来执行，例如type：1 是等待0.5s
        return SplashRequest(url=request.url, args={'wait': 0.5})

    def _requests_to_follow(self, response):
        """重写的函数哈！这个函数是Rule的一个方法
        :param response: 这货是啥看名字都知道了吧（这货也是个字典，然后你懂的ｄ(･∀･*)♪ﾟ）
        :return: 追踪的Request
        """
        # *************请注意我就是被注释注释掉的类型检查o(TωT)o 
        # if not isinstance(response, HtmlResponse):
        #     return
        # ************************************************
        seen = set()
        # 将Response的URL更改为我们传递下来的URL
        # 需要注意哈！ 不能直接直接改！只能通过Response.replace这个魔术方法来改！并且！！！
        # 敲黑板！！！！划重点！！！！！注意了！！！ 这货只能赋给一个新的对象（你说变量也行，怎么说都行！(*ﾟ∀ﾟ)=3）
        # newresponse = response.replace(url=response.meta.get('real_url'))
        for n, rule in enumerate(self._rules):
            # 我要长一点不然有人看不见------------------------------------newresponse 看见没！别忘了改！！！
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r, response)


    # 解析详情页面获取抓取的数据
    def parse_item(self, response):
        item = self.config.get('item')
        if item:
            cls = eval(item.get('class'))()
            loader = eval(item.get('loader'))(cls, response=response)
            # 动态获取属性配置
            for key, value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'css':
                        loader.add_css(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'value':
                        loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *extractor.get('args')))
            yield loader.load_item()

