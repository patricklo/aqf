#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore') #忽略警告信息
import tushare as ts

print '###5. 策略优化思路'
'''
优化： 1. 过滤假信号： 如假黄金交叉 -> 金叉过后马上死叉
      2. 不是所有金叉都买入 -> 震荡市场，频繁波动    -> 满足一定的值
'''

print '####1. 数据准备'
#tushare数据
data = ts.get_k_data('hs300',start = '2010-01-01', end = '2017-06-30') [['date','close']]  #获取K线数据，数据类型为DataFrame

data.set_index('date', inplace=True)  #默认Index为自动生成的0-n的数字，手动设置为date， inplace=True表示取代原数据

data['SMA20'] = data['close'].rolling(10).mean() #计算20日平均线数据，即1-19天的值为空，第20天的值为前20天（1-20）的均值，第21天的值为2-21价格的均值....
data['SMA60'] = data['close'].rolling(60).mean() #计算60日平均线数据，同上原理


print '####2. 策略思路开发'
data['SMA10-SMA60'] = data['SMA20'] - data['SMA60']
SD = 50 #设定预期值，SMA10一定要高于SMA60大于等于SD，才做多

#因此，position有3个值， 0, 1, -1
data['position'] = np.where(data['SMA10-SMA60'] > SD, 1, 0)  #np.where()  产生交易信号
data['position'] = np.where(data['SMA10-SMA60'] < -SD, -1, data['position'])  #如果 < -SD, 保持原值
print data['position'].value_counts()  #统计各个值对应的数量

print '####3. 计算市场的收益（market_return）以及策略的年华收益(strategy_returns)， 并且可视化'

### 市场return(market_return) - 2.连续  ln(P(t)/P(t-1))  (下面做法）
data['market_return'] = np.log(data['close'] / data['close'].shift(1)) #.shift(1) 拿前一个数据，即前一天close价格。计算出收益
####策略return(strategy_return)
data['strategy_return'] = data['position'].shift(1) * data['market_return']
data[['market_return','strategy_return']].cumsum().apply(np.exp).plot(title='SMA strategy 2', figsize=(10, 6))   # 计算累计收益-》 returns cumulative sum(累计求和）, apply应用（np.exp)自然底数e
plt.show()




