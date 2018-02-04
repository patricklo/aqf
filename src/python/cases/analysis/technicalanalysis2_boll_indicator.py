# coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import talib as ta
import warnings

warnings.simplefilter('ignore')
import tushare as ts
from statsmodels.tsa.stattools import adfuller, coint


'''
Bolling indicator: 布林带指标

3条布林线： up, mid, low

升破up,但又跌破up线，则short
跌破low,但又升破low线， 则long
'''

'''1. 数据准备'''
stock_index = ts.get_k_data('hs300','2016-06-01','2017-06-30')
stock_index['date'] = pd.to_datetime(stock_index['date'])
stock_index.set_index('date',inplace=True)
#print stock.head()

#ta.BBANDS  - bolling bands 布林带指标
stock_index['upper'], stock_index['middle'], stock_index['lower'] = ta.BBANDS(np.asarray(stock_index['close']),
                                                                              timeperiod=20, nbdevup =2, nbdevdn =2, matype =0)
# fig = plt.figure(figsize=(10,6))
# plt.plot(stock_index['close'])
# plt.plot(stock_index['upper'], linestyle='--')
# plt.plot(stock_index['middle'], linestyle='--')
# plt.plot(stock_index['lower'], linestyle='--')
# plt.title('HS300 布林线BBANDS图')
# plt.legend()
# plt.show()

'''2. 交易信号和持仓信号'''

#昨天数据
stock_index['yes_close'] = stock_index['close'].shift(1)
stock_index['yes_lower'] = stock_index['lower'].shift(1)
stock_index['yes_upper'] = stock_index['upper'].shift(1)
#前2天数据
stock_index['daybeforeyes_close'] = stock_index['close'].shift(2)
stock_index['daybeforeyes_lower'] = stock_index['lower'].shift(2)
stock_index['daybeforeyes_upper'] = stock_index['upper'].shift(2)

'''2.1 信号 产生开仓 或 平仓'''
#开多(long)仓信号 : 前天收盘价低于下轨， 昨日收盘价高于下轨
stock_index['signal'] = np.where(np.logical_and(stock_index['daybeforeyes_close'] < stock_index['daybeforeyes_lower'], stock_index['yes_close'] > stock_index['yes_lower']),
                                 1, 0)

#开空（short)仓信号 : 前天日收盘价高于上轨，昨日日收盘价低于上轨
stock_index['signal'] = np.where(np.logical_and(stock_index['daybeforeyes_close'] > stock_index['daybeforeyes_upper'], stock_index['yes_close'] > stock_index['yes_upper']),
                                 -1, stock_index['signal'])

print stock_index.tail()
# 显示有问题 无法绘图？？
# fig = plt.figure(figsize=(10, 8))
# plt.subplot(2,1,1)
# plt.title('HS300 bolling bands 布林带图')
# plt.gca().axes.get_xaxis().set_visible(False)
# stock_index['close'].plot(figsize=(10,8))
# plt.plot(stock_index['upper'], linestyle='--')
# plt.plot(stock_index['middle'], linestyle='--')
# plt.plot(stock_index['lower'], linestyle='--')
# plt.legend()
# plt.subplot(2,1,2)
# plt.plot(stock_index['signal'],marker='o',linestyle='')
# plt.legend()
# plt.suptitle('HS300 bolling bands 布林带图')
# plt.show()


'''2.2 持仓(position) 产生信号后的持仓策略'''
#与cci策略不一样的持仓计算方法，好处:适应之后比较复杂的策略算法
position = 0
for item in stock_index.iterrows():
    if item[1]['signal'] == 1:
        position = 1
    elif item[1]['signal'] == -1:
        position = -1
    else:
        pass
    stock_index.loc[item[0], 'position'] = position