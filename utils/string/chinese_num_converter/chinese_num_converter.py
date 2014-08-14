# -*- coding: utf-8 -*-
#  Documentation for this module.
#  @first_date    20100914
#  @date          20110314 - Added a function to clean the white space for input data.
#  @author        Chihyuan
#  @version       - 1.0  [stable]
#                 - 0.13 [internal-test] added get_single_chinese_number function
#
#  @brief         This program supports to convert Chinese number to Arabic number.
#                 It alsh has some APIs to support convertation.
#                   - such as 一萬      => 10000
#                   -        1.2萬      => 12000.0
#                   -        一千零二十 =>  1020
#
from types import IntType, UnicodeType

##
#   This program is support to convert Chinese number to Arabic number.
#
class ChineseNumConverter:
    ##
    #  @brief       Created dictionary about Chinese number to Arabic number.
    #
    def __init__(self):
        self.ARABIC_NUM = {
            u'0' : u'零',
            u'1' : u'一',
            u'2' : u'二',
            u'3' : u'三',
            u'4' : u'四',
            u'5' : u'五',
            u'6' : u'六',
            u'7' : u'七',
            u'8' : u'八',
            u'9' : u'九',
            u'10': u'十'
        }

        self.CHI_NUM = {
            u'○'  : 0,
            u'一' : 1,
            u'二' : 2,
            u'三' : 3,
            u'四' : 4,
            u'五' : 5,
            u'六' : 6,
            u'七' : 7,
            u'八' : 8,
            u'九' : 9,

            u'零' : 0,
            u'壹' : 1,
            u'貳' : 2,
            u'兩' : 2,
            u'參' : 3,
            u'肆' : 4,
            u'伍' : 5,
            u'陸' : 6,
            u'柒' : 7,
            u'捌' : 8,
            u'玖' : 9,

            u'０' : 0,
            u'１' : 1,
            u'２' : 2,
            u'３' : 3,
            u'４' : 4,
            u'５' : 5,
            u'６' : 6,
            u'７' : 7,
            u'８' : 8,
            u'９' : 9
        }

        self.CHI_UNIT = {
            u'十' : 10,
            u'拾' : 10,
            u'百' : 100,
            u'佰' : 100,
            u'千' : 1000,
            u'仟' : 1000,
            u'万' : 10000,
            u'萬' : 10000,
            u'億' : 100000000,
            u'兆' : 1000000000000
        }

    ##
    #  @brief       It supports to clean white space in dirty address
    #
    def _clean_dirty(self, dirty_data):
        string_replace = lambda x: ''.join(x.split(' '))
        clean_data = string_replace(dirty_data)

        return clean_data

    ##
    #  @brief       It can sum of Arabic number and Chinese number.
    #  @brief       such as: 12萬 => 120000
    #  @param       (Float) Arabic number
    #  @return      (Float) Arabic number
    #
    def _get_full_arabic_number(self, arabic_number_combine):
        if self.unit:
            arabic_number_combine = arabic_number_combine * self.unit
            self.unit = 0

        return arabic_number_combine

    ##
    #  @brief       A convertsation Chinese number to Arabic number.
    #  @param       (String-Unicode) Chinese Number or Arabic number
    #  @return      (Float) Arabic number
    #
    def get_arabic_number(self, number_str):
        number_str = self._clean_dirty(number_str)

        one_num_list = list(number_str)
        self.unit = 0
        digit_temp = []   #store digit stack

        arabic_number = [] #store arbic number stack

        ### filter dirty words - choose first number###
        # such as : '34+ABC5' => '34'
        found_number_list = []
        for every_number in one_num_list:
            if every_number.isdigit() or every_number in ['.', ','] or every_number in self.CHI_NUM or every_number in self.CHI_UNIT:
                found_number_list.append(every_number)
                one_num_list = found_number_list
            else:
                break
        #-filter

        arabic_combine_word_status = "Init"  # Remember the digit number status is Arabic number or Chinese number.
        total_div_count = 0 # count Arabic number to change Chinese number times for division.

        while one_num_list:
            one_word = one_num_list.pop()
            try: #It is a int or float number
                if(one_word == '.'):
                    arabic_number.append(one_word)
                    continue

                one_word = str(one_word)
                int(one_word)            #try to check the word is Arabic number or Chinese number

                arabic_combine_word_status = "Arabic Number"

                arabic_number.append(one_word)

                if(len(one_num_list) == 0):      #Next digit doesn't have any words
                    temp=''.join(arabic_number)
                    if len(temp) > 0:
                        arabic_number_combine = float(temp[::-1])   #temp=abcd => dcba
                    else:
                        return None     #When we Can't catch any input about number

                    digit_temp.append(self._get_full_arabic_number(arabic_number_combine))
                else:
                    continue
            except: #It is a word not a int or float number

                if self.CHI_UNIT.has_key(one_word):
                    self.unit = self.CHI_UNIT.get(one_word)
                    if self.unit == 10000:
                        digit_temp.append('w')      #萬
                        self.unit = 1
                    elif self.unit == 100000000:
                        digit_temp.append('y')      #億
                        self.unit = 1
                    elif self.unit == 1000000000000: #兆
                        digit_temp.append('z')
                        self.unit = 1

                    ### This is to support '3萬5千元'  (arabic combine with Chinese word)
                    if arabic_combine_word_status == "Arabic Number":
                        total_div_count += 1
                        arabic_combine_word_status = "Chinese Number"
                    ###-this
                else:
                    arabic_number_combine = self.CHI_NUM.get(one_word) #It isn't a Chinese number, then forgive it.
                    if arabic_number_combine:
                        digit_temp.append(self._get_full_arabic_number(arabic_number_combine))
                    else:
                        if(len(one_num_list)==0):      #Next digit doesn't have any words
                            temp = ''.join(arabic_number)
                            if len(temp) > 0:
                                try:
                                    arabic_number_combine = float(temp[::-1])   #temp=abcd => dcba
                                except:
                                    return None
                            else:
                                return None #When we Can't catch any input is number

                            digit_temp.append(self._get_full_arabic_number(arabic_number_combine))
                        else:
                            continue

        if self.unit == 10:    #deal with 十, not 十萬 and 二十 (only include 10~19)
            digit_temp.append(10)

        summary_number = 0
        tmp = 0

        while digit_temp:
            x = digit_temp.pop()
            if x == 'w':
                tmp *= 10000
                summary_number += tmp
                tmp = 0
            elif x == 'y':
                tmp *= 100000000
                summary_number += tmp
                tmp=0
            elif x == 'z':
                tmp *= 1000000000000
                summary_number += tmp
                tmp = 0
            else:
                tmp += x
        summary_number += tmp

        ### This is to support '3萬5千元'  (arabic combine with Chinese word)
        if total_div_count:
            summary_number = summary_number / (10 ** total_div_count)
        ###-this

        return summary_number

    ##
    #  @brief       A conversion from Chinese number such as 一九九五 not 一千一百九十五 to Arabic number.
    #  @param       (String-Unicode) Chinese Number or Arabic number
    #  @return      (Int) Arabic number
    #
    def get_single_arabic_number(self, number_str):
        number_str = self._clean_dirty(number_str)

        one_num_list = list(number_str)

        single_arabic_number_list = []
        arabic_number_combine = None

        while one_num_list:
            one_word = one_num_list.pop()
            try:
                singleArabicNumber = int(one_word)        #is Chinese number?
            except:
                singleArabicNumber = self.CHI_NUM.get(one_word)

            if isinstance(singleArabicNumber, IntType):
                single_arabic_number_list.append(str(singleArabicNumber))

        temp = ''.join(single_arabic_number_list)
        if temp:
            try:
                arabic_number_combine = int(temp[::-1])
            except:
                return None

        return arabic_number_combine

    ##
    #  @brief       A convertsation Arabic number to Chinese number such as 1234 => 一二三四
    #  @param       (Int) Arabic number
    #  @return      (String) Chinese number
    #
    def get_single_chinese_number(self, arabNumber):
        arabNumber = self._clean_dirty(arabNumber)

        output = ''
        is_seq = False

        if isinstance(arabNumber, IntType):
            str_num = str(arabNumber)
        elif isinstance(arabNumber, UnicodeType):
            str_num = arabNumber.encode('utf8')

        for every_number in str_num:
            if every_number in self.ARABIC_NUM:
                output += self.ARABIC_NUM[every_number]
                is_seq = True
            else:
                if is_seq:
                    break
                else:
                    continue

        if not output == '':
            return output
        else:
            return None
