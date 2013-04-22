# -*- coding: utf-8 -*-
#  @date        20120329
#  @author      grtfou
#  @version     - 1.0 [stable]
#  @brief       It is web crawling to get stock id by every category from Yahoo stock.
import urllib
from data_catcher.sources.conf.yahoo_conf import YahooConf

class CategoryCrawler:
    # data_type only 'daily' and 'weekly'
    def get_stock_id(self, category_id, crawling_domain='yahoo'):
        if crawling_domain == 'yahoo':
            from data_catcher.sources.yahoo_stock import YahooStock
            stock_crawler = YahooStock()
        else:
            sys.exit()

        search_list = []
        if category_id in YahooConf.STOCK_CATEGORY:
            url = YahooConf.CATEGORY_URL + urllib.quote_plus(YahooConf.STOCK_CATEGORY[category_id].encode('big5'))
            stock_items = stock_crawler.get_stock_id(url)

        return stock_items

### Unit test ###
'''
if __name__ == '__main__':
    my_tester = CategoryCrawler()
    print my_tester.get_stock_id('14')
'''
###-unit