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
CCI: ??全称？
'''

stock = ts.get_h_data('600030','2016-06-01','2017-06-30')
stock.sort_index(inplace=True)
#print stock.head()

##计算CCI, 取时间周期为20 (ta-lib集成很多技术指标函数)
stock['cci'] = ta.CCI(np.asarray(stock['high']), np.asarray(stock['low']), np.asarray(stock['close']), timeperiod=20)

#plt.subplot(2,1,1) #子图
#plt.title('600030 CCI indicator')
#plt.gca().axes.get_xaxis().set_visible(False) #不显示横轴
#stock['close'].plot(figsize=(10,6))
#plt.legend()
#plt.subplot(2,1,2)
#stock['cci'].plot(figsize=(10,2))
#plt.legend()
#plt.show()

''' 2. 交易信号 持仓信号和策略逻辑'''

stock['yes_cci'] = stock['cci'].shift(1)
stock['daybeforeyes_cci'] = stock['cci'].shift(2)

'''2.1 信号 产生开仓 或 平仓'''
#开多仓信号： 当前2日CCI小于-100，前1日CCI大于-100， 则是开多仓信号
stock['signal'] = np.where(np.logical_and(stock['daybeforeyes_cci']<-100,stock['yes_cci']>-100), 1, np.nan)

#开空仓信号： 当前2日CCI大于100，前1日CCI小于100, 则是开空仓信号
stock['signal'] = np.where(np.logical_and(stock['daybeforeyes_cci']>100, stock['yes_cci']<100), -1, stock['signal'])

#画图显示
# plt.subplot(3,1,1)
# plt.title('600030 CCI position')
# plt.gca().axes.get_xaxis().set_visible(False)
# stock['close'].plot(figsize=(12,12))
# plt.legend(loc='upper left')
#
# plt.subplot(3,1,2)
# stock['cci'].plot(figsize=(12,12))
# plt.legend(loc='upper left')
# plt.gca().axes.get_xaxis().set_visible(False)
#
# plt.subplot(3,1,3)
# stock['signal'].plot(figsize=(12,12), marker='o', linestyle='')
# plt.legend(loc='upper left')
#
# plt.show()


'''2.2 持仓 产生信号后的持仓策略'''
stock['signal'] = stock['signal'].fillna(method='ffill') #在下一个开仓信号前， 均沿用前一个开仓信号
stock['signal'] = stock['signal'].fillna(0)


# #画图显示
# plt.subplot(3,1,1)
# plt.title('600030 CCI position')
# plt.gca().axes.get_xaxis().set_visible(False)
# stock['close'].plot(figsize=(12,12))
# plt.legend(loc='upper left')
#
# plt.subplot(3,1,2)
# stock['cci'].plot(figsize=(12,12))
# plt.legend(loc='upper left')
# plt.gca().axes.get_xaxis().set_visible(False)
#
# plt.subplot(3,1,3)
# stock['signal'].plot(figsize=(12,12), marker='o', linestyle='')
# plt.legend(loc='upper left')
#
# plt.show()


'''3. 策略收益'''

stock['pct_chage'] = stock['close'].pct_change()
stock['strategy_return'] = stock['pct_chage'] * stock['signal']  #.shift(1) 不用shift(1),因前面已经shift过

#实际股票的累计收益
stock['actual_cum_return'] = (stock['pct_chage']+1).cumprod()

#策略股票的累计收益
stock['strategy_cum_return'] = (1+ stock['strategy_return']).cumprod()

stock[['actual_cum_return','strategy_cum_return']].plot(figsize=(12,6))
plt.show()