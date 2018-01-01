#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore')
import tushare as ts

'''
Momentum 动量效应 指在一定时期内，如果某股票或证券
（1） time-series  过去涨 未来一段时间内也会涨
（2） cross-sectional 横切面数据， 同一行业，有几个股票涨得好，未来预测也会涨得比较好；本来涨得不好的，未来也涨得不好

关注问题： 1. 过去的期限 ？？算涨得好
          2.
          
Strategy 思想： 前提：持有1天 ----》 交易频率高
1. 过去期限 1天
2. 优化：
    （1）过去5天平均收益
    （2）同时画出过去10天 20天 30天的平均收益
    （3）高频数据
'''

data = ts.get_k_data('hs300',start='2010-01-01',end='2017-12-14')[['date','close']]
data = pd.DataFrame(data)
data.rename(columns={'close':'price'}, inplace=True)
data.set_index('date',inplace=True)
#print data.head()


print '###############Momentum Strategy1: 最简单实现 （ 过去期限：1 天， 前一天涨就买）'

data['returns'] = np.log(data['price']/data['price'].shift(1))
data['position'] = np.sign(data['returns'])   # >0 sign 返回 1
#print data.head()

data['strategy'] = data['position'].shift(1) * data['returns']

#可视化，回测
#data[['returns','strategy']].cumsum().apply(np.exp).plot(figsize=(10,6))
#plt.show()


print '#################Momentum Strategy2: 优化 （1） 过去5天的平均收益'
data['returns_5d'] = data['returns'].rolling(5).mean()
data['position_5d'] = np.sign(data['returns_5d'])
data['strategy_5d'] = data['position_5d'].shift(1) * data['returns']

#data[['returns','strategy_5d']].dropna().cumsum().apply(np.exp).plot(figsize=(10,6))
#plt.show()


print '##############Momentum Strategy3: 参数寻优 --- 使用离散return 计算方法'

'''
连续return 公式 ： ln(p_t/p_t-1)
连续累计return:  e^(ln(p/p_t-1)1 + ln(p/p_t-1)2 + ... + )  e和ln抵消, 得出 -》 (p/p_t-1) * (p_t+1/p_t) * ... *
               即： data[['returns','strategy_5d']].dropna().cumsum().apply(np.exp)

离散return 公式 ： (p_t/p_t-1) - 1
离散累计return:    (1+ 离散return).cumprod() #累计相乘

'''

#data['returns_dis'] = data['price']/data['price'].shift(1)-1 #方法1
data['returns_dis'] = data['price'].pct_change() #方法2

data['returns_dis_cum'] = (data['returns_dis']+1).cumprod()
#print data.head()

price_plot = ['returns_dis_cum']

for days in [10,20,30,60]:
    price_plot.append('sty_cumr_%dd' % days)
    data['position_%dd' % days] = np.where(data['returns'].rolling(days).mean()>0, 1, -1)
    data['strategy_%dd' % days] = data['position_%dd' % days].shift(1) * data['returns']
    data['sty_cumr_%dd' % days] = (data['strategy_%dd' % days]+1).cumprod()
print data[price_plot].head()

data[price_plot].dropna().plot(title='HS300 Multi Parameters Momentum Strategy',figsize=(10,6), style=['--','--','--','--','--'])
plt.show()



print '##############Momentum Strategy4: 使用较高频的数据'
h300_hf = ts.get_k_data('hs300',ktype='5')  #ktype=5:5分钟数据
h300_hf.set_index('date',inplace=True)
h300_hf.index = h300_hf.index.to_datetime()

print h300_hf['2017-07-15':'2017-07-28'].head()

#策略实现 与上面相同
###h300_hf['returns'] =
