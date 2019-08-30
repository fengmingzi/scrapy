from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

# rules = {
#     'china': (
#         # 获取详情链接
#         Rule(LinkExtractor(allow='article\/.*\.html', restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]',
#                            tags=('a', 'area'), attrs=('href',)), callback='parse_item'),
#         # 获取下一页规则，设置process_request是为了解决有些页面是异步加载，因此这里集成了splash
#         Rule(LinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contains(., "下一页")]'), process_request='splash_request')
#     )
#     # 可以增加其它的规则。。。
#
# }

class SpiderRules:
    def __init__(self, allow=(), detailUrlXpaths=(), pageXpaths=(), detailTags=('a', 'area'), detailAttrs=('href',), detailCallback=None, isSplash=False):
        self.rules = {
            'ruleHref': (
                # 获取详情链接
                Rule(LinkExtractor(allow=allow, restrict_xpaths=detailUrlXpaths, tags=detailTags, attrs=detailAttrs), callback=detailCallback),
                # 获取下一页规则，设置process_request是为了解决有些页面是异步加载（比如需要滚动条滚动），因此这里集成了splash
                Rule(LinkExtractor(restrict_xpaths=pageXpaths), process_request='splash_request' if isSplash else None)
            ),
            'ruleClick': (
                # 获取详情链接
                Rule(LinkExtractor(allow=allow, restrict_xpaths=detailUrlXpaths, tags=detailTags, attrs=detailAttrs), callback=detailCallback),
            )
        }

