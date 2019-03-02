#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore') #忽略警告信息
import tushare as ts
import seaborn as sns
import quandl

#解决中文标题显示问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


'''
策略思想 ：(原始论文 ： https://www.nature.com/articles/srep01684)
1. 如果当周google搜索关键字 'debt' 的搜索量 > 过去三周平均，则做空道琼斯指数,持仓一周
2. 反之，则做多，持仓一周
'''

print '#####选择1.1 读取并使用论文的数据 （https://www.nature.com/articles/srep01684）'
paper = pd.read_csv('paper_data.csv', sep=' ', parse_dates=True)
data = pd.DataFrame(
    {'Google_week': paper['Google End Date'],
     'Debt':paper['debt'],
     'Date':paper['DJIA Date'],
     'DJCLOSE':paper['DJIA Closing Price'].astype(np.float64)}
)

data['Date'] = pd.to_datetime(data['Date'])
data['Google_week'] = pd.to_datetime(data['Google_week'])

print '#####选择1.2 读取并使用google的数据 (从google trend中可以下载csv'
trends_google = pd.read_csv('debt_google_trend.csv')
trends_google['Week'] = trends_google['Week'].apply(lambda x:pd.to_datetime(x.split(' ')[-1]))


all_data = pd.merge(data,trends_google,left_on='Google_week',right_on='Week')
all_data.drop('Week', inplace=True, axis=1)
all_data.set_index('Date', inplace=True)
all_data.rename(columns= {'Debt':'Debt_paper','debt':'Debt_download'}, inplace=True)

#验证论文上的debt数据（列：Debt_paper)与google下载的debt数据（列：Debt_download)是相关的
both_trends = all_data[['Google_week', 'Debt_paper', 'Debt_download']].set_index('Google_week')
print both_trends.corr()  #correlation