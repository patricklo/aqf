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
本代码对应 -> 5.三大经典策略_3.均值回归策略_1

基本思想：
1. 高抛 低买

缺点：
1. 不适合大牛市，-》 一直涨，但均值回归策略是预期会回归均值

均值回归策略 -> 
1. time-series 策略
    涨得高的股票会回归
    跌得多的股票会有上涨
2. cross-sectional 横切面数据 同一行业
    如同一行业30只股票
        涨得好的股票，未来可能跌，回归均值   -> long
        跌的股票，未来可能涨，回归均值      -> short
实现原理：
1. 价格与SMA值对比，设置偏离值，大于偏离值，则做空
                            小于偏离值，则做多
'''

a= pd.DataFrame([np.NaN,1,1,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,np.NaN,0,0])
a.ffill()
a.bfill()
print a.ffill().fillna(0)


print '####1. 数据准备'
data = ts.get_k_data('hs300',start = '2010-01-01', end = '2014-06-30') [['date','close']]
data.rename(columns={'close':'price'}, inplace=True)
SMA = 50
data['SMA'] = data['price'].rolling(SMA).mean()
threshold = 250
data['distance'] = data['price'] - data['SMA']

#data['distance'].dropna().plot(figsize=(10,6), legend=True)
#plt.axhline(threshold, color='r')  #画水平线
#plt.axhline(-threshold, color='r')
#plt.axhline(0, color='r')
#plt.show()

print '####2. 策略思路开发'

#####解决什么时候开仓问题
data['position'] = np.where(data['distance']>threshold,-1,np.nan)
data['position'] = np.where(data['distance']<threshold,1,data['position'])
######解决什么时候平仓的问题
'''
平仓条件：
当distance超过SMA时，即当前distance是正值，上一个distance是负值
                    或当前dis是负值，上一个是正值
就应该平仓 - 信号： 0
'''
data['position'] = np.where(data['distance'] * data['distance'].shift(1) < 0, 0, data['position'])

data['position'] = data['position'].ffill().fillna(0)
'''
ix[SMA:] ->
'''
#data['position'].ix[SMA:].plot(ylim=[-1.1,1.1], figsize=(10,6))
#plt.show()


print '####3. 计算市场的收益（market_return）以及策略的年华收益(strategy_return)， 并且可视化'
data['market_return'] = np.log(data['price']/data['price'].shift(1))
data['strategy_return'] = data['position'].shift(1) * data['market_return']
data[['market_return','strategy_return']].dropna().cumsum().apply(np.exp).plot(figsize=(10,6))
plt.show()