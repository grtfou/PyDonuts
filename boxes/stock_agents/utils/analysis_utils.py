# -*- coding: utf-8 -*-
#  @date        20120109
#  @author      grtfou
#  @version     - 0.1 [test]
#  @brief       It support some tools to analyze price and volume by stocks.

import datetime

class AnalysisUtils:
    def __init__(self):
        pass

    ##
    #  @brief       It supports to find date of minimum volume.
    #  @param       (Map) Stocks (Format: {stock_id:{date:{inf:}}})
    #  @param       (String) Stock id
    #  @return      (Map) price/vol of stock by minimum volume.
    def get_min_volume(self, stock_collection, stock_id):
        stock_data = stock_collection[stock_id]['data']
        min = -1
        lowest_date = ""

        for date in stock_data:
            if min == -1:
                min = float(stock_data[date]['volume'])

            print date, stock_data[date]['volume']
            if float(stock_data[date]['volume']) < min:
                min = float(stock_data[date]['volume'])
                lowest_date = date

        return stock_data[lowest_date]

    ##
    #  @brief       It supports to find multi dates of high volume.
    #  @param       (Map) Stocks (Format: {stock_id:{date:{inf:}}})
    #  @param       (String) Stock id
    #  @param       (String) price/volume type ("daily" or "weekly")
    #  @param       (Int) How many high vols do you want to find? (Default:1)
    #  @return      (Map) price/vol of stock by first date.
    #  @return      (Map) price/vol of stock by high volume date
    def get_last_max_volume(self, stock_collection, stock_id, type="weekly", max_vol_times=1):
        stock_data = stock_collection[stock_id]['data']

        # Init
        last_highest_vol_date = ""
        max_volume = -1
        now_inf = ""
        high_vol_output = []

        date_index = 0
        for date in sorted(stock_data, reverse=True):
            #print "Track:\t%s\t\t\t%s" % (date, stock_data[date]['volume'])
            point_volume = int(stock_data[date]['volume'])
            if date_index == 0: #first date
                date_index += 1
                now_inf = [{'date':date, 'inf': stock_data[date]}]
                continue

            date_index += 1
            if point_volume > max_volume:
                max_volume = point_volume
            else:
                increase_day = 0
                if type == 'daily':
                    increase_day = 1
                else:
                    increase_day = 7

                last_highest_vol_date = (datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=increase_day)).strftime("%Y-%m-%d")
                if last_highest_vol_date in stock_data:
                    if max_vol_times == 1:
                        high_vol_output.append({'date':last_highest_vol_date, 'inf':stock_data[last_highest_vol_date]})
                        break
                    else:
                        max_vol_times -= 1
                        max_volume = 0
                        high_vol_output.append({'date':last_highest_vol_date, 'inf':stock_data[last_highest_vol_date]})

        return now_inf, high_vol_output