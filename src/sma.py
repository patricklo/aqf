# -*- coding: utf8 -*-
import numpy as np
import pandas_test as pd
import tushare as ts
import matplotlib.pyplot as plt

data = ts.get_k_data('hs300', start = '2010-01-01', end='2017-06-30')

data = pd.DataFrame(data)


data.rename(columns={'close': 'price'}, inplace=True)


data.set_index('date', inplace = True)


data['SMA_10'] = data['price'].rolling(10).mean()

data['SMA_60'] = data['price'].rolling(60).mean()

print data.tail()

data[['price','SMA_10','SMA_60']].plot(title='HS300 stock price | 10 & 60 days SMAs',
                                      figsize=(10, 6))
plt.show()

data['position'] = np.where(data['SMA_10'] > data['SMA_60'], 1, -1)

data.dropna(inplace=True)

#data['position'].plot(ylim=[-1.1, 1.1], title='Market Positioning')
#plt.show()

data['returns'] = np.log(data['price'] / data['price'].shift(1))
# data['returns_dis'] = data['price']/data['price'].shift(1)-1    #离散计算return方法1
# data['return_dis2'] = data['price'].pct_change()                #离散计算return方法2

#data['returns'].hist(bins=35)
#plt.show()

data['strategy'] = data['position'].shift(1) * data['returns']
#注意未来函数；一般会使得回测收益高估；

data[['returns', 'strategy']].sum()

#data[['returns', 'strategy']].cumsum().apply(np.exp).plot(figsize=(10, 6))   #可视化；离散的计算方法参考Momoentum策略
#plt.show()

data[['returns', 'strategy']].mean() * 252     #年化收益率；
data[['returns', 'strategy']].std() * 252 ** 0.5   #年化风险；
data['cumret'] = data['strategy'].cumsum().apply(np.exp)
data['cummax'] = data['cumret'].cummax()

data[['cumret', 'cummax']].plot(figsize=(10, 6))
plt.show()