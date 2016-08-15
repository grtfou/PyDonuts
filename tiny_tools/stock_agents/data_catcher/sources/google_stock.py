# -*- coding: utf-8 -*-
#  @date        20120329
#  @author      grtfou
#  @version     - 1.0 [Stable]
#  @brief       It is web crawling to get stock price/vol from Google stock.
#  @brief       http://www.google.com/finance
#  @brief       http://www.google.com/finance/historical?q=

import sys
import urllib
import datetime

from lxml import etree
from StringIO import StringIO

from base_template import BaseTemplate

class GoogleStock(BaseTemplate):
    def get_stock_inf(self, stock_id, data_type):
        url = "http://www.google.com/finance/historical?q=TPE:%s&histperiod=%s" % (stock_id, data_type)
        parse_rule = './/table[@class="gf-table historical_price"]//tr//td'

        parse_result = self._get_crawling_text(url, parse_rule)


        stock = {}
        stock[stock_id] = {}
        stock[stock_id]['data'] = {}
        price_col_count = 0
        date_temp = {}
        date = ""
        for record in parse_result:
            tag_class = record.values()[0]
            value = record.text.strip().lower()
            if tag_class == 'lm':
                date = datetime.datetime.strptime(value, '%b %d, %Y').strftime('%Y-%m-%d')
            elif tag_class == 'rgt rm':
                date_temp['volume'] = str(int(value.replace(',', '')) / 1000)
            elif tag_class == 'rgt':
                if price_col_count == 0:
                    date_temp['open'] = value
                    price_col_count += 1
                elif price_col_count == 1:
                    date_temp['high'] = value
                    price_col_count += 1
                elif price_col_count == 2:
                    date_temp['low'] = value
                    price_col_count += 1
                elif price_col_count == 3:
                    date_temp['close'] = value
                    price_col_count = 0

            stock[stock_id]['data'][date] = date_temp.copy()

        return stock
