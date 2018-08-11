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
本代码对应 -> 4.三大经典策略_2.动量策略momemtum_1

动量交易策略Momentum -> 
1. time-series 策略
    强者越强
2. cross-sectional 横切面数据 同一行业
    如同一行业30只股票
        涨得好的股票，未来可能继续涨   -> long
        跌的股票，未来可能继续跌      -> short

考虑因素
1. 过去  -> 多久的过去

strategy思想： 前提：
1. 过去1天， 涨的   -> long
   过去1天， 跌的   -> short
2. Momentum策略的前提都是持有股票1天  -> 可能导致交易次数频繁

优化思路：
1.过去时间的调整，以及持有时间的调整
2.同时考虑过去不同时间段的情况，如过去10天，20天，30天
3.高频数据 -> 过去5分钟数据会不会好一点 

'''

print '####1. 数据准备'
data = ts.get_k_data('hs300',start = '2010-01-01', end = '2017-06-30') [['date','close']]

data.rename(columns={'close':'price'},inplace=True)
data.set_index('date',inplace=True)

print '####2. 策略思路开发'
data['market_return'] = np.log(data['price'] / data['price'].shift(1))
data['position'] = np.sign(data['market_return'])

print '####3. 计算市场的收益（market_return）以及策略的年华收益(strategy_return)， 并且可视化'
data['strategy_return'] = data['position'].shift(1) * data['market_return']
#data[['market_return','strategy_return']].cumsum().apply(np.exp).plot(title='动量策略 - Momentum Strategy', figsize=(10,6))

print '###4. 策略收益的风险评估'


print '###5. 策略优化'
##解决：交易次数过于频繁
##优化1. 从看过去1天的数据  -> 看过去5天的数据
data['mean_5days'] = data['market_return'].rolling(5).mean()
data['position_mean_5days'] = np.sign(data['mean_5days'])
data['strategy_return_5days'] = data['position_mean_5days'].shift(1) * data['market_return']
#data[['market_return','strategy_return','strategy_return_5days']].dropna().cumsum().apply(np.exp).plot(title='动量策略 - Momentum Strategy (5 days)', figsize=(10,6))

##优化2：参数寻优

##优化3：使用高频一些的数据 如：分钟，秒级数据
hs300_hf = ts.get_k_data('hs300',ktype='5')
hs300_hf.set_index('date',inplace=True)
hs300_hf.index = hs300_hf.index.to_datetime()

hs300_hf['market_return'] = np.log(hs300_hf['close']/hs300_hf['close'].shift(1))
hs300_hf['position'] = np.sign(hs300_hf['market_return'].rolling(30).mean())
hs300_hf['strategy_return'] = hs300_hf['position'].shift(1) * hs300_hf['market_return']
hs300_hf[['market_return','strategy_return']].dropna().cumsum().apply(np.exp).plot(figsize=(10,6))

plt.show()
