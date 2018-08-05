#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore') #忽略警告信息
import tushare as ts


'''
本代码对应 -> 1.三大经典策略_1.简单移动平均线策略SMA

SMA（Simple Moving Average)简单移动平均线策略，也叫双均线模型，主要逻辑：拿长期(i.e. 60天均线）和短期（ie.20天均线）两条线进行对比 
      黄金交叉golden cross： 短期线升穿长期线   ->   buy
      死亡交叉dealth cros： 短期线跌穿长期线    ->  sell

优化： 1. 过滤假信号： 如假黄金交叉 -> 金叉过后马上死叉
      2. 不是所有金叉都买入

'''

print '####1. 数据准备'
#tushare数据
data = ts.get_k_data('600030',start = '2010-04-01', end = '2016-11-01')   #获取K线数据，数据类型为DataFrame
#data = pd.DataFrame(data)  #转换data数据为DataFrame, 因为tushare接口返回的就是DF数据类型，故不需要此行

#print data.head()  #head() 输出前面几条数据（默认前5条），可省略

data.set_index('date', inplace=True)  #默认Index为自动生成的0-n的数字，手动设置为date， inplace=True表示取代原数据
data.rename(columns={'volume':'Quantity'}, inplace=True)

#print data.info()  #输入data里的数据信息


data['SMA20'] = data['close'].rolling(10).mean() #计算20日平均线数据，即1-19天的值为空，第20天的值为前20天（1-20）的均值，第21天的值为2-21价格的均值....
data['SMA60'] = data['close'].rolling(60).mean() #计算60日平均线数据，同上原理

#data[['close','SMA20','SMA60']].plot(title='HS300 20 & 60 SMAs', figsize=(10,6))  #将3条线画出来，并显示/可视化
#plt.show()


print '####2. 策略思路开发'
data['position'] = np.where(data['SMA20'] > data['SMA60'], 1, -1)  #np.where()  产生交易信号
data.dropna(inplace=True) #删除空值
#data['position'].plot(ylim=[-1.1,1.1], title='Market position', figsize=(10,6))


print '####3. 计算市场的收益（returns）以及策略的年华收益(strategy_returns)， 并且可视化'

'''
return算法：
1.离散 （P(t) / P(t-1)）-1
2.连续  ln(P(t)/P(t-1))  (下面做法）
'''
### 2.连续  ln(P(t)/P(t-1))  (下面做法）
data['returns'] = np.log(data['close'] / data['close'].shift(1)) #.shift(1) 拿前一个数据，即前一天close价格。计算出收益

####1.离散 （P(t) / P(t-1)）-1
data['returns_dis1'] = data['close'] / data['close'].shift(1)
data['returns_dis2'] = data['close'].pct_change() #作用同上

###return可视化
#data['returns'].hist(bins=50)  #bins:粗细度设置



####策略 strategy
'''
目的： 确认做空时，收益计算是正确的
  做空： -1 * 正return  结果：负  -> 说明是亏的
  做空： -1 * 负return  结果：正  -> 说明是赚的
'''
data['strategy_return'] = data['position'].shift(1) * data['returns']

'''
持有期收益returns 跟SMA策略的收益strategy_return对比 
'''
print data[['returns','strategy_return']].sum()

#data[['returns','strategy_return']].plot(figsize=(10,6))                                                                 #np.log() -> 连续return
#data[['returns','strategy_return']].cumsum().apply(np.exp).plot(figsize=(10, 6))   # 计算累计收益-》 returns cumulative sum(累计求和）, apply应用（np.exp)自然底数e
'''
即 e ^[ln(P(t)/P(t-1)+ln(P(t+1)/P(t)+...+]  = e ^ ln(P(t)/P(t-1)) * e ^ ln(P(t+1)/P(t)) * ... *   -> e 和 ln抵消
    = [P(t)/P(t-1)] * [P(t+1)/P(t)] * ... * 最终结果  ->>>>累计收益
'''

print '###4. 策略收益的风险评估'
'''
1.最大收益
2.计算回撤时间
'''

#年化收益 * 252
data['returns_annualized'] = data['returns'].mean() * 252
data['strategy_return_annualized'] = data['strategy_return'].mean() * 252

#年化标准差 * 252开根号  ( ** 0.5)
print data[['returns','strategy_return']].std() * 252 ** 0.5

#累计收益
data['cum_return'] = data['strategy_return'].cumsum().apply(np.exp)
data['cum_max'] = data['cum_return'].cummax() #cummax -> 累计求和中的最大值， 即代表
#data[['cum_return','cum_max']].plot(figsize=(10,8))

#计算回撤
drawdown = (data['cum_max'] - data['cum_return'])  #每天的回撤
print drawdown.max()  #寻找最大回撤

#计算最大回撤的持续时间 -> 从上一个最大回撤到下一个最大回撤的时间段periods
temp = drawdown[drawdown == 0]
periods = (temp.index[1:].to_datetime() - temp.index[:-1].to_datetime())
print periods[12:25]
print periods.max()


#plt.show()


print '###5. 策略优化思路'
'''
优化： 1. 过滤假信号： 如假黄金交叉 -> 金叉过后马上死叉
      2. 不是所有金叉都买入 -> 震荡市场，频繁波动
'''

print '2_sma.py'



