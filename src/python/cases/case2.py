#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore')
import tushare as ts

##获取沪深300的股票列表
##获取估值低的  PE PB 低， 以行业区分
hs300 = ts.get_gem_classified()['code'].tolist()  ## get_hs300s() 出错， 用其它替代先
print hs300[:10]

##获取股票基本面数据
stock_basics = ts.get_stock_basics()
stock_basics.reset_index(inplace=True)   ##重置索引Index 变成原始状态 index是0.......N

data1 = stock_basics.loc[stock_basics['code'].isin(hs300),['code','name', 'industry', 'pe', 'pb', 'esp', 'rev','profit',]]
data1.columns=['code','name','industry','PE','PB','EPS','收入%','利润%']
print data1.head()

###获取盈利能力数据
stock_profit = ts.get_profit_data(2017,1)  #年份 + 季度
data2 = stock_profit.loc[stock_profit['code'].isin(hs300),['code','roe','gross_profit_rate','net_profit_ratio']]
data2.columns =['code','ROE','毛利率','净利率']
#data2 = round(data2,2)   #round
print data2.head()


###获取成长能力数据
stock_growth = ts.get_growth_data(2017,1)
data3 = stock_growth.loc[stock_growth['code'].isin(hs300),['code','nprg']]
data3.columns = ['code','NI增长率']
print data3.head()

from functools import reduce

merge = lambda x,y: pd.merge(x,y, how='left', on='code')
data = reduce(merge,[data1,data2,data3])
data.drop_duplicates(inplace=True)
print data.head()


#估值系数： 烟蒂  PE*PB 越小说明估值低 有潜力

data['估值系数'] = data['PE'] * data['PB']
print data.head()


#按条件选股
data_filtered = data.loc[(data['估值系数'] < 60) & (data['ROE'] > 1)]
data_filtered.sort_values(['估值系数'],ascending=True, inplace=True)

print data_filtered.head()
print '筛选结果共 %d' % len(data_filtered)


def map_func(x):
    if x['ROE'] > 3:
        return '成长'
    elif x['ROE'] >=0:
        return '低成长'
    return '亏损'

data['成长性'] = data.apply(map_func,axis=1)
print data.head()


data_growth = data[data['成长性'] == '高成长'].sort_values(['估值系数'],ascending=True)
print data_growth




###下一步，按行业分类  groupby

def group_by(df):
    return df.sort_values(['估值系数'],ascending=True)[:2]

data_grouped = data.groupby('成长性')
print data_grouped.size()

data_grouped = data.groupby('成长性').apply(group_by)
print data_grouped


data_grouped = data.groupby('industry').apply(group_by)
print data_grouped
