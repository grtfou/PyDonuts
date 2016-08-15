# -*- coding: utf-8 -*-
#  @date        20111228
#  @author      grtfou
#  @version     - 0.1 [test]
#  @brief       It is web crawling to get stock price/vol from Google stock.

import urllib

from lxml import etree
from StringIO import StringIO

class BaseTemplate:
    def _get_crawling_text(self, url, parse_rule, encoding='utf8'):
        stock_web = urllib.urlopen(url)
        stock_html_context = stock_web.read()#.decode(encoding)
        stock_web.close()

        my_html_parser = etree.HTMLParser()
        context_tree = etree.parse(StringIO(stock_html_context), my_html_parser)

        parse_result = context_tree.xpath(parse_rule)

        return parse_result

    def get_price_vol(self, stock_id, data_type='daily'):
        pass
