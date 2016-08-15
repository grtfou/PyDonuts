# -*- coding: utf-8 -*-
#  @date        20120110
#  @author      grtfou
#  @version     - 0.1 [test]
#  @brief       It is the main program by stock system.

import sys

from utils.analysis_utils import AnalysisUtils
from data_catcher.histories_crawler import HistoriesCrawler

alert_line_times = 4

if __name__ == '__main__':
    if sys.argv > 1:
        stock_id = sys.argv[1]

        if sys.argv < 3:
            pv_type = 'weekly'
        else:
            pv_type = sys.argv[2]
    else:
        print "Please give me stock id!"
        sys.exit()

    my_analysis = AnalysisUtils()
    my_histories_crawler = HistoriesCrawler()

    stock_d = my_histories_crawler.get_price_histories(stock_id, 'daily')
    stock_user_type = my_histories_crawler.get_price_histories(stock_id, pv_type)
    now_inf, some_inf = my_analysis.get_last_max_volume(stock_user_type, stock_id, pv_type, alert_line_times)

    least_date = sorted(stock_d[stock_id]['data'], reverse=True)[0]
    now_price = stock_d[stock_id]['data'][least_date]['close']
    support_pressure_price = some_inf[0]['inf']['high']

    print "=====%s(%s)=====" % (stock_id, pv_type)
    print "Now price:[%s]" % now_price
    print "Alert price:%s" % support_pressure_price
    if now_price > support_pressure_price:
        print "*** > Buy ***"
        for alert_line in xrange(1, alert_line_times):
            print some_inf[alert_line]['date'], some_inf[alert_line]['inf']
    elif now_price == support_pressure_price:
        print "<Be careful>"
    else:
        print "!!! < Sell !!!"