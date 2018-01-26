# coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings

warnings.simplefilter('ignore')
import tushare as ts
from statsmodels.tsa.stattools import adfuller, coint

'''
pair trading 类别：   ->> 统计套利

1. AH股：价差
2. 内外盘：跨市场
3. 同行业的不同股票
4. ETF

前提：需要cfa 二级知识


简单的思路:
  同行业股票A,B：
  A,B价差的mean， 波动超过一定界限，就认为有套利机会   <----跟mean_reversion策略类似

策略风险：
   极端变化：某一个公司重大变化，导致价格不再遵守均值回归的规则， 如果说某一个公司有重大发明， 则会引起这个公司的价格一直上涨，而同行业的别的公司不涨


使用的前提：
 1. 数据平稳性：stationary   -》要求有点高； 
  如果数据不平稳 non-stationary -> （1）进行拆分  A：delta=P_t - P_t-1  B： delta = P_t - P_t-1 (即价格可能不平稳，但价格变化可能是平稳的）
                                  (2) co-integration 协整关系（课程使用的方法）,  AB绑定？栓绳子？-> 找到线性组合关系 ： ax+by=f(x,y)

'''

'''
#2 复杂方法  <--靠谱
改进： 不断rebalance - 》》 不断调整两只股票价差的均值
--》strategy5_pair_trading2.py

#方法1的缺点
1. 没有检验数据是否stationary 
2. 假设priceDelta是符合normal正态分布
3. 用了未来的spread


#方法2 改进点：
1，考虑了stationary
2. PriceDelta不同处理

#方法2原理, (方法1是直接用x-y) spread作为z-score
y = ax + b + ε
得出
ε = y - ax - b
 
 ε符合正态分布（白噪声）  -> z-score 

3.

'''

m = np.array([1,2,3,4,5])
n = m * 5 + 2
slope,intercept = np.polyfit(m,n,1).round(2)  #回归 1：代表是1元方程 2：是2元方程
#print slope,intercept

data1 = ts.get_k_data('600199', start='2013-06-01', end='2014-12-31')[['date','close']]
date2 = ts.get_k_data('600702', start='2013-06-01', end='2014-12-31')[['date','close']]
data = pd.concat([data1,date2], axis=1)

data.set_index('date', inplace=True)
stock_pair = ['600199', '600702']
data.columns = stock_pair
#print data.head()

data.corr()  #计算方差 协方差
#plt.figure(figsize=(10,6))
#plt.title('stock correlation')
#plt.plot(data['600199'],data['600702'],'.')
data.dropna(inplace=True)
#plt.show()

[slope,intercept] = np.polyfit(data.iloc[:,0],data.iloc[:,1],1).round(2)
#print slope,intercept

#ε = y - ax - b
data['spread'] = data.iloc[:,1] - (data.iloc[:,0]*slope + intercept)
#data['spread'].plot(figsize=(10,6))
#plt.show()    #画图

#标准化spread -》 zscore  =  (spread - mean(spread)) / σ(spread) 标准差sigma
data['zscore'] = data['spread'] - data['spread'].mean() / data['spread'].std()
#data['zscore'].plot(figsize=(10,6))
#plt.axhline(1.5)
#plt.axhline(0)
#plt.axhline(-1.5)
#plt.show()

##根据zscore 产生交易信号, y:701, x:199
#positon_1: 199 position_2:702
data['position_1'] = np.where(data['zscore']>1.5,1,np.nan)
data['position_1'] = np.where(data['zscore'] <-1.5, -1, data['position_1'])
data['position_1'] = np.where(data['zscore'] < 0.5, 0 , data['position_1'])

data['position_1'] = data['position_1'].fillna(method='ffill')
#data['position_1'].plot(ylim=[-1.1,1.1], figsize=(10,6), title='Trading Signal Uptrade')

data['position_2'] = -np.sign(data['position_1'])
#data['position_2'].plot(ylim=[-1.1,1.1],figsize=(10,6), title="Trading Signal Downtrade")
#plt.show()


#策略年化收效和可视化
data['return_600199'] = np.log(data['600199']/data['600199'].shift(1))
data['return_600702'] = np.log(data['600702'] / data['600702'].shift(1))

data['return_strategy'] = 0.5*(data['position_1'].shift(1)*data['return_600199']) + 0.5*(data['position_2'].shift(1) * data['return_600702'])

data[['return_600199','return_600702','return_strategy']].dropna().cumsum().apply(np.exp).plot(figsize=(10,6), title='Strategy Backtesting')
plt.show()
