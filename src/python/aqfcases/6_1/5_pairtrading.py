#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore') #忽略警告信息
import tushare as ts

#解决中文标题显示问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


'''
本代码对应 -> 8.配对交易_1. 原理

A股和H股套利： 同一公司在分别在A和H股上市
内外盘： 同上，跨市场
同行业的两只股票： 有内在关系，数据平稳（stationary, )


pair trading : 1. stationary - 
2. non-stationary 


'''

print '####1. 数据准备'
data = ts.get_k_data('hs300',start = '2010-01-01', end = '2017-06-30') [['date','close']]

data.rename(columns={'close':'price'},inplace=True)
data.set_index('date',inplace=True)

print '####2. 策略思路开发'



print '####3. 计算市场的收益（market_return）以及策略的年华收益(strategy_return)， 并且可视化'


print '###4. 策略收益的风险评估'


print '###5. 策略优化'


