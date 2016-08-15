# -*- coding: utf-8 -*-
#  @date        20120110
#  @author      grtfou
#  @version     - 0.1 [test]
#  @brief       It is the main program by stock system.

import sys

from stock_selector import StockSelector

if __name__ == '__main__':
    category_set = []
    if sys.argv > 1:
        category_set = list(set(sys.argv[1].split(',')))

    limit_setting = {'max_vol_times': 2,
                     'stock_categories': category_set,
                     'price_higher_limit': 50,
                     'price_lower_limit' : 1,
                     'vol_lower_limit' : 10000}

    my_selector = StockSelector()
    my_selector.red_head_index(limit_setting, 'weekly', 'yahoo')