# -*- coding: utf-8 -*-
#  @date        20111228
#  @author      grtfou
#  @version     - 0.1 [test]
#  @brief       It is web crawling to get stock price/vol from yahoo stock.
#  @brief       http://hk.finance.yahoo.com/

import sys
import urllib
import datetime

from lxml import etree
from StringIO import StringIO

from base_template import BaseTemplate

class YahooStock(BaseTemplate):
    ##
    #  @brief       It supports to get stock items (id and stock name).
    #  @return      (Map) id: stock name
    def get_stock_id(self, url):
        parse_rule = './/form[@name="stock"]//table//tr//td//a'
        parse_result = self._get_crawling_text(url, parse_rule, 'big5')

        stock_items = {}
        for record in parse_result:
            tag_class = record.values()[0]
            value = record.text

            if tag_class == 'none' and value:
                stock_inf = value.split(" ")
                stock_items[stock_inf[0].strip()] = stock_inf[1].strip()

        return stock_items

    def get_stock_inf(self, stock_id, data_type):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month - 1
        day = datetime.datetime.now().day
        if data_type == 'daily':
            url = "http://finance.yahoo.com/q/hp?s=%s.TW&c=%s&a=%s&b=%s&f=%s&d=%02d&e=%s&g=d" % (stock_id, year-1, month, day, year, month, day)
        else:
            url = "http://finance.yahoo.com/q/hp?s=%s.TW&c=%s&a=%s&b=%s&f=%s&d=%s&e=%s&g=w" % (stock_id, year-1, month, day, year, month, day)

        parse_rule = './/tr//td[@class="yfnc_tabledata1"]'
        parse_result = self._get_crawling_text(url, parse_rule)

        stock = {}
        stock[stock_id] = {}
        stock[stock_id]['data'] = {}
        date_temp = {}
        date = ""

        index = 0
        for record in parse_result:
            tag_class = record.values()[0]
            if record.text is None:
                continue
            else:
                value = record.text.strip().lower()

            if value.count('dividend'):
                index = 0
                continue

            if index == 0:
                if value == '*':
                    break
                date = datetime.datetime.strptime(value, "%b %d, %Y").strftime("%Y-%m-%d")
                index+=1
            elif index == 1:
                date_temp['open'] = value
                index+=1
            elif index == 2:
                date_temp['high'] = value
                index+=1
            elif index == 3:
                date_temp['low'] = value
                index+=1
            elif index == 4:
                date_temp['close'] = value
                index+=1
            elif index == 5:
                date_temp['volume'] = str(int(value.replace(',', '')) / 1000 * 5)
                index+=1
            elif index == 6:
                index = 0

            stock[stock_id]['data'][date] = date_temp.copy()

        return stock
