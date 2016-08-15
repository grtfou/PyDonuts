# -*- coding: utf-8 -*-
#  @date        20120110
#  @author      grtfou
#  @version     - 0.1 [test]
#  @brief       It support some tools to select stocks that can buy.

from data_catcher.categories_crawler import CategoryCrawler
from data_catcher.histories_crawler import HistoriesCrawler
from utils.analysis_utils import AnalysisUtils

class StockSelector(object):
    ##
    #  @brief       It supports to find multi dates of high volume.
    #  @param       (Map) Stocks (Format: {stock_id:{date:{inf:}}})
    #  @param       (String) Stock id
    #  @param       (String) price/volume type ("daily" or "weekly")
    #  @param       (Map) Limit set (format: {price_higher_limit:30, vol_lower_limit:1000 ...}
    #  @return      (Map) price/vol of stock by first date.
    #  @return      (Map) price/vol of stock by high volume date
    def red_head_index(self, limit_setting, type='weekly', crawling_domain='yahoo'):
        ### Init ###
        category_search_list = []

        max_vol_times = limit_setting['max_vol_times']
        stock_categories = limit_setting['stock_categories']

        price_higher_limit = limit_setting['price_higher_limit']
        price_lower_limit = limit_setting['price_lower_limit']
        vol_lower_limit = limit_setting['vol_lower_limit']
        ###-init

        my_category_crawler = CategoryCrawler()
        my_histories_crawler = HistoriesCrawler()
        my_analysis = AnalysisUtils()

        for category_id in stock_categories:
            stock_items = my_category_crawler.get_stock_id(category_id)
            for stock_id in stock_items:
                print "==========%s==========" % (stock_id)
                stock = my_histories_crawler.get_price_histories(stock_id, type, crawling_domain)
                now_inf, some_inf = my_analysis.get_last_max_volume(stock, stock_id, type, max_vol_times)

                if len(now_inf) > 0 and len(some_inf) > 0:
                    ### limit ###
                    now_price = float(now_inf[0]['inf']['close'])
                    before_price = float(some_inf[0]['inf']['high'])
                    now_vol = int(now_inf[0]['inf']['volume'])

                    if (now_price < price_lower_limit) or (now_price > price_higher_limit) or (now_vol < vol_lower_limit) or (now_price < before_price):
                        continue
                    ###-limit

                    print now_inf
                    for a in some_inf:
                        print a

