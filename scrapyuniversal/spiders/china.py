# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyuniversal.items import *
from scrapyuniversal.loaders import *
from scrapy_splash import SplashRequest


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['http://tech.china.com/articles/']
    
    rules = (
        Rule(LinkExtractor(allow='article\/.*\.html', restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contains(., "下一页")]'), process_request='splash_request')
    )

    def splash_request(self, request):
        """
        :param request: Request对象（是一个字典；怎么取值就不说了吧！！）
        :return: SplashRequest的请求
        """
        # dont_process_response=True 参数表示不更改响应对象类型（默认为：HTMLResponse；更改后为：SplashTextResponse）
        # args={'wait': 0.5} 表示传递等待参数0.5（Splash会渲染0.5s的时间）
        # meta 传递请求的当前请求的URL
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
                yield rule.process_request(r)



    def parse_item(self, response):
        loader = ChinaLoader(item=NewsItem(), response=response)
        loader.add_xpath('title', '//h1[@id="chan_newsTitle"]/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('text', '//div[@id="chan_newsDetail"]//text()')
        loader.add_xpath('datetime', '//div[@id="chan_newsInfo"]/text()', re='(\d+-\d+-\d+\s\d+:\d+:\d+)')
        loader.add_xpath('source', '//div[@id="chan_newsInfo"]/text()', re='来源：(.*)')
        loader.add_value('website', '中华网')
        yield loader.load_item()
