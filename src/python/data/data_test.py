#coding:utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import tushare as ts
import warnings
warnings.simplefilter('ignore')


# data = ts.get_k_data('600030', start='2016-01-01', end='2017-01-01')
#
# print data.tail()

def multistocks(tickers):

    def data(ticker):
        stocks = ts.get_k_data(ticker, start= '2016-1-1', end='2017-1-1')
        stocks.set_index('date', inplace=True)
        stocks.set_index = pd.to_datetime(stocks.index)
        return stocks

    datas = map(data, tickers)
    return pd.concat(datas,keys=tickers, names=['Ticker','Date'])

tickers = ['600030','000001', '600426']
all_stocks = multistocks(tickers)
#print all_stocks


close_price = all_stocks[['close']].reset_index()  #重置索引
#print close_price

daily_close = close_price.pivot(index ='Date', columns='Ticker', values='close') #表转置
#print daily_close

#daily_close.plot(figsize=(8,6))    #一张大图显示3个stock

#daily_close.plot(figsize=(10,8), secondary_y='600030')    #3个stock子图 拼接，避免用上面的方式，当股票价格差距太大时，图片不好看

#daily_close.plot(subplots=True, figsize=(10,8))    #3个stock子图 拼接，避免用上面的方式，当股票价格差距太大时，图片不好看
#plt.show()

price_change = daily_close / daily_close.shift(1) - 1
daily_close['yesterday'] = daily_close['000001'].shift(1)
print price_change.ix[:, 0:3].head()

price_change2 = daily_close.pct_change()
print price_change2.ix[:,0:2].head()


cum_daily_return = (1 + price_change).cumprod()

#print cum_daily_return.head()

# cum_daily_return.plot()
# plt.show()


zxzq = price_change['600030']
#
# zxzq.hist(bins=50, figsize=(8,6))  #直方图
# plt.show()
#
# zxzq.describe()

# print zxzq.describe(percentiles=[0.025,0.5,0.975])

# _ = price_change.hist(bins=20, sharex=True, figsize=(8,9)) #直方图
# plt.show()

# print '##### QQ plots   #####'
# import scipy.stats as stats
# fig = plt.figure(figsize=(7,5))
# ax=fig.add_subplot(111)
# stats.probplot(zxzq, dist='norm', plot=ax)  #有error: 'Text' object is not callable
# plt.show()


hs300 = ts.get_k_data('hs300', start='2016-1-1', end='2017-1-1')
hs300.set_index('date', inplace=True)
hs300.set_index = pd.to_datetime(hs300.index)
hs300_return = hs300['close'].pct_change().fillna(0)
return_all =pd.concat([hs300_return, price_change2], axis=1)
return_all.rename(columns={'close':'hs300'}, inplace=True)

print return_all.head()

cummulative_return_all=(1 + return_all).cumprod()

#cummulative_return_all[['hs300','600030','600426']].plot(figsize=(8,6))
#plt.show()

# 相关性
# corrs = return_all.corr()
# fig = plt.figure(figsize=(8,6))
# seaborn.heatmap(corrs)
# plt.show()


print '######多个股票间的相关性  ######'
# plt.figure(figsize=(8,6))
# plt.title('Stock Correlations')
# plt.plot(daily_close['600030'],daily_close['000001'],'.')
# plt.xlabel('600030')
# plt.ylabel('000001')
# plt.show()







