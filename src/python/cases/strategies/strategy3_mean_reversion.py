#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore')
import tushare as ts

'''
Mean Reversion均值反转： 一只股票一直涨，长期来看会下跌回归均值； 相反股票一直跌，长期看也会上涨回归均值

具体策略： 
    简单： 同一行业，看观察期（如：30天SMA），与Price对比，选出几只涨得最好（看跌） 和 几只跌得最多的（看涨）
    
    适用于： 震荡市场，不适合牛市
'''

#NaN空值处理
#NaN在计算策略信号时特别有用，
d = pd.DataFrame([1, np.NaN, np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,1,1])
print d.ffill().fillna(0)  #向前填充,直到下一个非NaN值为止？ -》

d = pd.DataFrame([np.NaN, 1, np.NaN, np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,1,1])
print d.ffill().fillna(0)  #fillna把第一个NaN填充为0

data = ts.get_k_data('hs300', start = '2010-01-01', end='2014-06-30')[['date','close']]  #避免2015大牛市
data.rename(columns={'close':'price'},inplace=True)
data.set_index('date',inplace=True)

data['returns'] = np.log(data['price'] / data['price'].shift(1))

SMA = 50

data['SMA'] = data['price'].rolling(SMA).mean()
threshold = 250

data['distance'] = data['price'] - data['SMA']

#data['distance'].dropna().plot(figsize=(10,6),legend=True)
#plt.axhline(threshold, color='r')  # axhline:画水平直线
#plt.axhline(-threshold, color='r')
#plt.axhline(0, color='r')
#plt.show()

#data['position'] = np.sign(data['distance']-threshold)
data['position'] = np.where(data['distance'] > threshold,-1,np.nan)  #价格过高，应做空
data['position'] = np.where(data['distance'] < -threshold, 1, data['position']) #价格过低，做多； 不符合条件的： data['position'] 保持原值不变
#以上只解决了开仓信号问题
#以下解决开仓 什么时候卖出平仓的问题

#平仓思路： 当价格回到均值（SMA50）时，就是应该平仓的信号 -> position=0

#判断价格回到均值， 当distance*上一个distance为负值时，代表经过了均值(SMA50）
data['position'] = np.where(data['distance'] * data['distance'].shift(1) < 0, 0, data['position'])

data['position'] = data['position'].ffill().fillna(0)

data['position'].ix[SMA:].plot(ylim=[-1.1,1.1], figsize=(10,6))
plt.show()









