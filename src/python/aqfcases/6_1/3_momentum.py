#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore') #忽略警告信息
import tushare as ts


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




print '####2. 策略思路开发'


print '####3. 计算市场的收益（returns）以及策略的年华收益(strategy_returns)， 并且可视化'



print '###4. 策略收益的风险评估'




print '###5. 策略优化思路'





