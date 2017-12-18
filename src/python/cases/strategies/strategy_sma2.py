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


print '### 一： 策略开发思路 ###'

data['position'] = np.where(data['SMA20']>data['SMA60'], 1, -1)
data.dropna(inplace=True)  #去掉空值

#data['position'].plot(ylim=[-1.1,1.1], title='market positioning')
#plt.show()




print '## 二： 计算策略收益 及 可视化 ###'

data['returns'] = np.log(data['close']/data['close'].shift(1))  #连续的return
#离散的return？
data['returns_dis'] = data['close']/data['close'].shift(1) - 1
#离散的retur2： pd.pct_changes()   data['close'].pct_change()

# data['returns'].hist(bins=35)
# plt.show()


data['strategy'] = data['position'].shift(1) * data['returns']
## position * return 得出策略收益  shift(1) 取昨天的position： 因为今天的position，收盘后才能确定； 故需要用昨天的position   <----  未来函数的问题

'''
未来函数问题：
  现在用未来的数据 => 影响收益（产生理所当然的收益）
  如多因子模型：
    2014 2015 2016 2017（现在）财务数据
    2015年需要用2014的财务数据，因为站在2015年时候的情形，2015财务数据是不知道的。
  
'''
#data[['returns','strategy']].sum()    ##回测： returns历史实际收益  strategy策略的收益： 没有算compound
#data[['returns','strategy']].cumsum().apply(np.exp).plot(figsize=(10,6))## compound算法：复利
#plt.show()
'''
回测可视化： returns历史实际收益  strategy策略的收益

.cumsum().apply(np.exp).
前面return strategy: ln(p/p_t-1)

cumsum: ln(p/p_t-1)1 + ln(p/p_t-1)2 ...
apply(np.exp): e^ln(p/p_t-1)1 + ln(p/p_t-1)2 ...

e^ln(p/p_t-1)1 + ln(p/p_t-1)2  =>>>    e^ln 抵消 得出 =》》  (p_t/p_t-1)*(p_t+1/p_t)*.......

用意： ？？？？


现实情况： 因为中国市场不允许做空，因此无法达到预期收益

'''



print '### 三： 策略收益风险评估 ###'

#年化收益
print data[['returns','strategy']].mean() * 252 #转换成年化收益 252个交易日

#年化风险
#年化标准差std = daily std * 252开根号 即（252 ** 0.5）     252/255都可以
print data[['returns','strategy']].std() * 252 ** 0.5


'''
最大回撤 drawdown.max, 原理：

即产品价格从最高点跌到最低点的最大幅度： 历史最高 - 历史最低

告诉投资者，有可能的最大损失

'''
#1. 首先计算策略的累计收益
data['cumret'] = data['strategy'].cumsum().apply(np.exp)
#2. 累计收益中的最大值
data['cummax'] = data['cumret'].cummax()
#data[['cumret','cummax']].plot(figsize=(10,6))
#plt.show()
#3. 求drawdown
drawdown = (data['cummax'] - data['cumret'])
#4. max drawdown
print drawdown.max()

#5. 计算从前一个max drawdown(旧高点）开始下跌 到 恢复到这个max drawdown的时间

temp = drawdown[drawdown==0]  #drawdown == 0  即data['cummax'] = data['cumret'] 即累计收益达到历史最大回撤点 即处于max drawdown的时候

periods = (temp.index[1:].to_datetime() - temp.index[:-1].to_datetime())  # 从1 : N 减 0 :（N-1)

print '#计算从前一个max drawdown(旧高点）开始下跌 到 恢复到这个max drawdown的时间'
print periods.max()




print '### 四： 策略优化思路 ###'
'''
原有思路：

    1. 产生 signal  （现实中应该用事件驱动（优矿平台），才能不停地计算）
    
    问题： （1） 在市场震荡时，频繁产生signal  -》 优化： 产生signal时， 再判断价格是否超过一定距离 再决定是否开仓买入/卖出
              但其实会对问题1的优化 会导致信号产生慢
'''

print '### 问题（1）优化策略 ###'

hs300 = ts.get_k_data('hs300', '2010-01-01','2017-06-30')[['date','close']]
hs300 = pd.DataFrame(hs300)
hs300.rename(columns={'close':'price'}, inplace=True)
hs300.set_index('date', inplace=True)
print hs300.head()

hs300['SMA10'] = hs300['price'].rolling(10).mean()
hs300['SMA60'] = hs300['price'].rolling(60).mean()

print hs300[['price','SMA10','SMA60']].tail()

#hs300[['price','SMA10','SMA60']].plot(grid=True, figsize=(10,6))
#plt.show()

hs300['10-60'] = hs300['SMA10'] - hs300['SMA60']

SD = 60  ###判断价格是否超过一定距离，设定为50, 缺点： 反应较慢
hs300['regime'] = np.where(hs300['10-60'] > SD, 1, 0)
hs300['regime'] = np.where(hs300['10-60'] < SD, -1, hs300['regime'])
print hs300['regime'].value_counts()  ##统计信号次数： -1 多少次， 1 多少次， 0 多少次

hs300['MarketRealReturn'] = np.log(hs300['price']/hs300['price'].shift(1))
hs300['StrategyReturn'] = hs300['regime'].shift(1) * hs300['MarketRealReturn']

### 别以为图形不错， 这策略就可以， 并没有加上交易手续费等其它因素
hs300[['MarketRealReturn','StrategyReturn']].cumsum().apply(np.exp).plot(grid=True,figsize=(10,6))
plt.show()














