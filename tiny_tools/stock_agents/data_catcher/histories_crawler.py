# -*- coding: utf-8 -*-
#  @date        20120329
#  @author      grtfou
#  @version     - 1.0 [Stable]
#  @brief       It is web crawling to get stock price/vol from web.

import sys

class HistoriesCrawler:
    # data_type only 'daily' and 'weekly'
    def get_price_histories(self, stock_id, data_type='daily', crawling_domain='yahoo'):
        if crawling_domain == 'google':
            from data_catcher.sources.google_stock import GoogleStock
            stock_crawler = GoogleStock()
        elif crawling_domain == 'yahoo':
            from data_catcher.sources.yahoo_stock import YahooStock
            stock_crawler = YahooStock()
        else:
            sys.exit()

        stock = stock_crawler.get_stock_inf(stock_id, data_type)

        return stock

### Unit test ###
'''
if __name__ == '__main__':
    my_tester = HistoriesCrawler()
    print my_tester.get_price_histories(6116, 'weekly', 'yahoo')
    print my_tester.get_price_histories(6116, 'weekly', 'google')
'''
###-unit