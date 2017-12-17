#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore')
import tushare as ts

###
print '#### 1.移动平均策略（双均线 低胜率 高收效） 2.动量交易策略 3. 均值反转策略 4.Pair Trading 统计套利策略 ###'

'''
1.双均线策略：MA：movement average
  不同时间的均线间的交叉：如20天均线和60天均线
  golden cross : 金叉 买入： 20MA 上穿 60MA
  death cross: 死亡交叉 卖出： 20MA 跌穿 60MA
  
'''



