# -*- coding: utf-8 -*-
#  @brief         This program can test many cases in chinese_num_converter API.
from chinese_num_converter import ChineseNumConverter

my_num_converter = ChineseNumConverter()
test_data = [u'九',
             u'十一',
             u'一百二十三',
             u'一千二百零三',
             u'一万一千一百零一',
             u'十万零三千六百零九',
             u'一百二十三万四千五百六十七',
             u'一千一百二十三万四千五百六十七',
             u'一億一千一百二十三万四千五百六十七',
             u'一百零二億五千零一万零一千零三十八',
             u'一千一百一十一兆一千一百二十三万四千五百六十七',
             u'一兆一千一百一十一億一千一百二十三万四千五百六十七',
             u'1.2萬',
             u'2.4',
             u'3600',
             u'兩',
             u'一千',
             u'一千零二十',
             u'十坪',
             u'1.4萬元',
             u'3,600NT',
             u'NT$3,600',
             u'十萬元',
             u'１０萬',
             u'八十八年',
             u'八八年',     #getSingleArabicNumber() handle
             u'88年',
             u'一九九五',   #getSingleArabicNumber() handle
             '25年',
             u'三十'.encode('utf8'),#can't know
             u' ',
             u'九 五汽油',
             u'3+1',
             u'三+一',
             u'一生一世',
             u'八千5百零2元',
             u'8千5百零2元',
             u'１仟20',
             u'1０二拾元',
             u'一二三萬零四元',
             u'一.二萬元',
             u'二點三萬元']


for numberString in test_data:
    print my_num_converter.get_arabic_number(numberString)
    #print my_num_converter.get_single_arabic_number(numberString)
