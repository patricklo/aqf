#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore')

print '###########  金融时间序列处理 #########'

print '#### python 自带 datetime #########'
now = datetime.now()
print now
print '{}年{}月{}日'.format(now.year,now.month,now.day)
print datetime.now() - datetime(2017, 11, 1)


dt_time = datetime(2017,6,18)
str_time = str(dt_time)
print str_time
print type(str_time)

str_time2 = dt_time.strftime('%d/%m/%Y')
print str_time2


dt_str = '2017-06-18'
dt_time = datetime.strptime(dt_str,'%Y-%m-%d')
print dt_time
print type(dt_time)

from dateutil.parser import parser
dt_str = '18-06-2016'
dt_time2 = parser(dt_str)
print dt_time2
print type(dt_time2)


print '#3##### pandas 的datetime'
str_time = pd.Series(['2016/06/18'],name='timesss')
dt_time = pd.to_datetime(str_time)
print type(str_time)
print type(dt_time)


dates = [datetime(2016,9,1),datetime(2017,9,1)]

print pd.DatetimeIndex(dates)

dates = ['2016,8,3', '2016,8,5']
date_time = pd.DatetimeIndex(dates)  #把python下的date_time转换成pandas的时间索引datetimeIndex

print date_time   ####DateTimeIndex


dates = pd.date_range('8/1/2014', periods=10)  ##date_range生成从8/1/2014开始共10天的DatetimeIndex的数据
print dates
df = pd.Series(np.random.randn(10), index=dates)
print df.index

#freq='M' 按月
tm_period = pd.period_range('2016-1-1',periods=12, freq='M')  ##perido_range生成是PeriodIndex的数据
#以PeriodIndex为索引创建Series
ps=pd.Series(np.random.randn(12),index=tm_period)
print ps.index


print '#############tushare 实例#######'
import tushare as ts
data = ts.get_k_data('000001','2015-01-01','2016-12-31')
data.index = pd.to_datetime(data['date'])
del data['date']
print data.head(5)

data_close_price = data['close']
print data_close_price.head(5)

print data_close_price['2016-01-01':'2016-01-05']

print data.loc['2016-01-04']


print data['2016-1'].head()  ###获取某月的数据， 如果需要具体日期数据需用.loc去获取
#print data['2016-01-04']  ###会出错，需用.loc去获取

print data['2016-1':'2016-2-15'].head()


print '########3时间序列的前后移动 ##############'

print data_close_price.head()

yes_close_price = data_close_price.shift(1) ###下移一天的收盘价格，所以2015-01-05的close是NaN,因为往前移了一天
print yes_close_price.head()

print '####计算收盘百分比######'
print (data_close_price/yes_close_price -1).head()

print '####时间序列的频率调整######'

sample = data_close_price.head(2)

#计算累积收益率
cum_return = (1 + (data_close_price/yes_close_price -1)).cumprod()
print cum_return.head()


print '2015年2月的平均收益：' , cum_return['2015-2'].mean()


print '#### resample 调整频率 #####'
print cum_return.resample('M',how='mean').head()

print '### resample:  ohlc: open price/highest price/lowest price/close price########'
print '#### 统计每个月的ohlc### '
print data_close_price.resample('M', how='ohlc').head()

print '####时间序列的频率转换######'

sample2 = cum_return[1:3]
print sample2

sample2_by_hour = sample2.resample('H')
sample2_by_hour.fillna(method = 'ffill')
print sample2_by_hour.head()
sample2_by_hour.interpolate() ##以线形方式填充空值
print sample2_by_hour.head()


print '@@@@@@@@@  数据频率转换的实战应用   @@@@@@@@@@@@@'
print '@@@ 因数据都是高频，都是秒级数据或更多， 但策略其实基于5分钟或者更长的价格，所以需要做频率转换 resample'

data = ts.get_tick_data('600030','2017-08-18')   ####tick data： 3秒一个价格 -》 频率太高
data.set_index('time', inplace=True)   ### tick 数据时间列是time
data.sort_index(ascending=True, inplace=True)
print data.head(10)

data.index=pd.to_datetime(data.index)  ## 把纯时间 转成 带日期的时间

#####   5T: 5分钟数据
data_5m = data.resample('5T')

print data_5m.head(10)

data_5m_price = data['price'].resample('5T', how='ohlc')
print data_5m_price.head(10)













