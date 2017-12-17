#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore')
import tushare as ts

###
print '#### 1.移动平均策略（双均线 低胜率 高收益） 2.动量交易策略 3. 均值反转策略 4.Pair Trading 统计套利策略 ###'

'''
1.双均线策略：MA：moving average
  不同时间的均线间的交叉：如20天均线和60天均线
  golden cross : 金叉 买入： 20MA 上穿 60MA
  death cross: 死亡交叉 卖出： 20MA 跌穿 60MA
'''

print '## 1.移动平均策略（双均线 低胜率 高收益） ##'
data = ts.get_k_data('600030', start='2010-01-01', end='2017-01-01')
data.set_index('date',inplace=True)
data['SMA20'] = data['close'].rolling(20).mean()
data['SMA60'] = data['close'].rolling(60).mean()
#data[['close','SMA20','SMA60']].plot(subplots=True,  figsize=(10,8))
#plt.show()


data['returns'] = np.log(data['close']/data['close'].shift(1))  #连续的return
#离散的return？
data['returns_dis'] = data['close']/data['close'].shift(1) - 1
#离散的retur2： pd.pct_changes()


data['position'] = np.where(data['SMA20']>data['SMA60'], 1, -1)

'''
    cumsum():累计求和 apply(np.exp):对所有值求自然底数 e^cum_return1 e^cum_return2... etc
'''
data['returns'].cumsum(0).apply(np.exp).plot(figsize=(10,6)) #可视化：计算累计收益，连续下的算法
plt.show()




