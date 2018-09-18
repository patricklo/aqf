# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np


df = pd.DataFrame(
    [6.68, 21.75, 75.85, 66.71, 23.77],
    index=['6000001','6000002','6000003','6000004','6000005'],
    columns=['PE']
)
print len(df), type(df)
print df.head(2)
print df.info()
print df.tail(2)


for i,j in enumerate(['a','b','c']):
    print (i,j)
a = zip([1,2,3],['a','b','c'])
print list(a)
for i,j in zip([1,2,3],['a','b','c']):
    print (i,j)
print list(map(str.upper,['a','python','c++']))


stock_data = pd.Series(
    {'2016/10/10':12.57,'2016/10/11':12.07,'2016/10/12':12.17,'2016/10/13':12.27,'2016/10/14':12.37,'2016/10/15':12.5,'2016/10/16':12.7,
     '2016/10/17':11.5,'2016/10/18':12.77,'2016/10/19':11.88,'2016/10/20':12.59,'2016/10/21':12.99,'2016/10/22':13,'2016/10/23':12.35}
)
print (stock_data.rolling(3).mean())  #3日移动平均值



####talib: 其它指标 MACD RSI 等
import talib as ta
ta.MA(np.array(stock_data),timeperiod=3)  #Talib的3日移动平均值 实现
ta.MACD(np.array(stock_data), signalperiod=3)  #MACD
ta.RSI(np.array(stock_data), signalperiod=3)  #MACD
