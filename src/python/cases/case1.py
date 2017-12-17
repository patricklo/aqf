#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore')
import tushare as ts

hs300 = ts.get_k_data('hs300',start= '2015-01-01', end='2017-10-31')
hs300.set_index('date', inplace=True)
hs300['close'].plot(figsize=(8,5),grid=True, title='HS300 Close Price')
#plt.show()

hs300['return'] = np.log(hs300['close']/hs300['close'].shift(1))  ### 连续收益：当天price/前一天price 再取对数np.log()？

print hs300[['close','return']].tail()

hs300[['close','return']].plot(subplots=True, figsize=(10,8), grid=True)
#plt.show()


print '@@@@@@@@@  SMA 移动平均值 @@@@@@@@@@'

#SMA 20天移动平均值 计算方法1
hs300['SMA20'] = hs300['close'].rolling(window=20).mean()  #rolling.mean(): 20天的价格取平均数
print hs300.tail()

#SMA 计算方法2  （pip install TA-Lib)
import talib as ta
hs300['SMA20_TALIB'] = ta.SMA(np.asarray(hs300['close']),20)
print hs300.tail()

#hs300[['close','SMA20','SMA20_TALIB']].plot(subplots=True, figsize=(10,8), grid=True)
#plt.show()

#hs300['SMA_60'] = hs300['close'].rolling(window=60, min_periods=0).mean() #### 60天SMA移动平均
## min_periods=0 : 可选参数 代表意思是第1天到第60天的SMA是有值的
## 如不设min_periods： 第1天到第60天的SMA为NaN
#hs300[['close','SMA20','SMA_60']].plot(subplots=True, figsize=(10,8), grid=True)
#plt.show()

#TA-Lib布林带
#hs300['Upper'],hs300['Middle'],hs300['Lower'] = ta.BBANDS(np.asarray(hs300['close']),timeperiod=20, nbdevup=2, nbdevdn=2)
#hs300[['Upper','Middle','Lower']].plot(figsize=(10,8))
#plt.show()






