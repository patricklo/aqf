#coding:utf-8
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

#检验数据是否stationary
#1. 直接看图 2.AR/MA/ARMA模型
'''
AR： auto regression 模型
y_t = b_0 + b_1 * y_t-1 + e

(1) 当b_1 = 1, -》 non-stationary

假设DF检验 -》 证明b_1是否等于1

或 ADF 检验（DF升级版） adfuller包


'''

'''
两个思路： （1）最简单的方法 -> 改进   (2) 协整关系
如；
600199
600702


'''

stock_pair=['600199','600702']
data1 = ts.get_k_data('600199','2013-06-01','2014-12-31')[['close','date']]
data2 = ts.get_k_data('600702','2013-06-01','2014-12-31')[['close']]
data = pd.concat([data1,data2],axis=1)
data.set_index('date',inplace=True)
data.columns = stock_pair
print data.head()

#data.plot(figsize=(10,6))
#plt.show()

#找到股票价差



data['priceDelta'] = data['600199'] - data['600702']
#data['priceDelta'].plot(figsize=(8,10))
#plt.ylabel('Spread')
#plt.axhline(data['priceDelta'].mean())
#plt.show()


'''
协整：standardized spread(z-score) 标准化价差
standardized(z-score) = (两只股票每天的spread - spread.mean()) / spread的标准差σ
'''
data['zscore'] = (data['priceDelta'] - np.mean(data['priceDelta'])) / np.std(data['priceDelta'])
#data['zscore'].plot(figsize=(8,10))
#plt.ylabel('zscore')
#plt.axhline(data['zscore'].mean())
#plt.show()

#开仓条件
#如果zscore > 1.56 short 600199 long 另一个
#    zscore < -1.56 long 600199 short另一个
print len(data[data['zscore'] < 1.5])

data['position_1'] = np.where(data['zscore'] > 1.5, -1, np.nan)  #-1：short 199，long另一个
data['position_1'] = np.where(data['zscore'] < -1.5, 1, data['position_1'])  #1： long 199, short另一个

#平仓条件 (0 可以调整，或者是某个正负值 如： +- 0.5
#1. 简单方法
  # 上一个zscore>0 下一个zsore<0 达到平仓条件
  #或上一个zscore < 0 下一个zsore > 0
#2. 更理想一点的方法 应该是event driven -> 即实时/每天调整
data['position_1'] = np.where(abs(data['zscore']) < 0.5, 0, data['position_1']) #设置平仓条件

data['position_1'] = data['position_1'].fillna(method='ffill')

data['position_2'] = -np.sign(data['position_1'])



#data['position_1'].plot(ylim=[-1.1, 1.1], figsize=(10,6))
#data['position_2'].plot(ylim=[-1.1, 1.1], figsize=(10,6))
#plt.show()


data['return_1'] = np.log(data['600199'] / data['600199'].shift(1))
data['return_2'] = np.log(data['600702'] / data['600702'].shift(1))

data['strategy'] = 0.5 * (data['position_1'].shift(1) * data['return_1']) + 0.5 * (data['position_2'].shift(1) * data['return_2'])

data[['return_1','return_2','strategy']].dropna().cumsum().apply(np.exp).plot(figsize=(10,6))
plt.show()




'''
#2 复杂方法
改进： 不断rebalance - 》》 不断调整两只股票价差的均值
--》strategy5_pair_trading2.py
'''
