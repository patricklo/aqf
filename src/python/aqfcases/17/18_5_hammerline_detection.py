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
本代码对应 -> 18. 量化投资与技术分析_5.形态识别和移动止损策略_2.锤子线形态识别

锤子线/上吊线 特征：
K线中， 实体线为中间长方形部分， 上影线为实体上方的直线部分， 下影线为实体下方的直线部分
（上涨： 红色， 实体上边界为收盘价，下边界为开盘价，上影线为当天最高价，下影线为当天最低价
  下跌： 绿色，实体上边界为开盘价，下边界为收盘价，上影线为当天最高价，下影线为当天最低价）
1. 中间实体小
2. 上影线短
3. 下影线长 （一般大于中间实体线3倍以上）



缺点：？？
'''


print '#####1. 数据获取和处理'
CODE = '002398'
BODY_SIZE=0.03  #锤子线实体线大小,波动范围%，不超过3%
HEAD_SIZE=0.5   #锤子线上影线大小,不能超过下影线长度的0.5倍
TAIL_SIZE=2     #锤子线下影线大小,大于实体线长度的2倍以上
LENGTH= 10      #观察周期
STOP_LOST_TRIGGER = 1  #止损值，倍数， 表示价格偏离均线满足几倍标准差时止损   mean- (1* σ)   --- σ： 标准差 standard deviation

data = ts.get_h_data(CODE,'2012-01-01','2017-01-01')
data.sort_index(ascending=True,inplace=True)

data.reset_index(inplace=True)   ###重设Index, 有默认数字为Index, 而非日期）
data['pct_change'] = data['close'].pct_change()
data['ma'] = data['close'].rolling(LENGTH).mean()
data['std'] = data['close'].rolling(LENGTH).std()
del data['volume']
del data['amount']
data['yesterday_ma'] = data['ma'].shift(1)   #前一天的移动平均值
data['yesterday_std'] = data['std'].shift(1) #前一天的标准差




print '#####2. 识别锤子形态和特征'

data['body'] = abs(data['close'] - data['open'])
data['head'] = data['high'] - data[['close','open']].max(axis=1)
data['tail'] = data[['close','open']].min(axis=1) - data['low']

data['body_condition'] = np.where(data['body']/data['open'] > BODY_SIZE, 0, 1)   #判断实体线大小,波动范围%，不超过3%
##判断上影线部分大小不超过下影线的0.5倍, 两步判断，先判断下影线是否等于0，等于0就没有意义进行下一步
data['head_condition'] = np.where(data['tail'] == 0, False, data['head'] / data['tail'] < HEAD_SIZE)
data['tail_condition'] = np.where(data['body'] == 0, True, data['tail'] / data['body'] > TAIL_SIZE) #判断下影线部分大小大于实体线的2倍


data['hammer'] = data[['body_condition','head_condition','tail_condition']].all(axis=1)
'''
.all: 当所有为true或!=0，才返回为true
.any: 任一值为true就可以返回true

axis=1 : 代表一天的值比较， 而非多天
'''

data['yesterday_hammer'] = data['hammer'].shift(1)  #避免未来数据问题，当天看前一天产生的信号即可


