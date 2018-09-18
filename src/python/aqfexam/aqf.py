# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np


#字符串格式化 小数点
strategy_return = 0.124173
##{位置参数:格式化形式}
print '{:.4f}'.format(strategy_return)
print '%.4f' %strategy_return
print '{1:.4f} is the return at {0}'.format('2018-08-01',strategy_return)
print '{time} is the return at {str_return}'.format(str_return=strategy_return, time='2018-08-01')

#Dictionary
factor_data = {'600001':1,'600002':22,'600003':333,'600004':4444,'600005':55555}
for pair in factor_data:
    print (pair)
for dict_key,dict_value in factor_data.items():
    print (dict_key,dict_value)
for dict_key in factor_data:
    print dict_key, factor_data[dict_key]
for dict_value in factor_data.values():
    print dict_value


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
#ta.MA(np.array(stock_data),timeperiod=3)  #Talib的3日移动平均值 实现
#ta.MACD(np.array(stock_data), signalperiod=3)  #MACD
#ta.RSI(np.array(stock_data), signalperiod=3)  #MACD


df = pd.DataFrame(
    [[25.4, 7.13, 0.9322],
     [23.1213, 5.9634, 0.9236],
     [20.7556, 311.7743, 1.0415],
     [22.4981, 9999, 0.8973],
     ],
    index= ['00001', '00002', '00003', '00004'],
    columns=['LCAP', 'PE', 'REVS20']
)
chosen_stock_codes = df[(df['PE'] < 20) & (df['LCAP'] >= 20) & (df['LCAP'] <= 25)].index
print list(chosen_stock_codes)
print (df[(df['PE'] < 20) & (df['LCAP'] >= 20) & (df['LCAP'] <= 25)])

chosen_data = pd.Series(
    [10, 11, 12, 13, 14],
    index= pd.date_range('2018-01-01',periods=5)
)
print chosen_data>12
print chosen_data[chosen_data>12]


dataFromFile = pd.read_csv('data.txt',index_col=0)
print dataFromFile
dataFromFile2 = pd.read_csv('data2.txt', index_col=0, sep=' ')
print dataFromFile2
#help(pd.read_csv)


'''
Information Ratio: IR = (Rp - Ri) / std_between_portfolio_benchmark
Sharpe Ratio:      SR = (Rp - Rf) / portfolio_std 
'''
df = pd.DataFrame(
    [[0.01, 0.02],
     [-0.02, 0.06],
     [0.01, 0.1],
     [0.03, 0.03]
     ],
    index = [pd.date_range('2018-01-01', periods=4)],
    columns= ['daily_return','benchmark_daily_return']
)
def calculate_information_ration(return_data):
    std_between_portfolio_benchmark = (return_data['daily_return'] - return_data['benchmark_daily_return']).std()
    return (return_data['daily_return'] - return_data['benchmark_daily_return']).mean() / std_between_portfolio_benchmark
def calculate_sharpe_ratio(return_data):
    portfolio_std = return_data['daily_return'].std()
    return (return_data['daily_return'] - return_data['benchmark_daily_return']).mean() / portfolio_std
print calculate_information_ration(df)
print calculate_sharpe_ratio(df)

sqr = lambda a:a ** 2
print sqr(4)

pd.date_range('2018-03-18', periods=5000)
pd.date_range(start='2018-03-18', end='2018-06-01', freq='2H')
pd.date_range(start='2018-03-18', end='2018-06-01', freq='2D')
pd.date_range(start='2018-03-18', end='2018-06-01', freq='B')  #business day
pd.date_range(start='2018-03-18', end='2018-06-01', freq='W-Mon') #only Monday

df = pd.DataFrame(
    [[15, 10, 11],
     [13, 11, 11],
     [10, 12, 11],
     [10, 13, 11],
     [13, 12, 11]
     ],
    index= [pd.date_range('2018-01-01', periods=5)],
    columns=['MA_5', 'MA_20', 'MA_60']
)
df['position'] = np.where((df['MA_5'] > df['MA_20']) & (df['MA_20'] > df['MA_60']), 1, -1)
print df

condition = np.array([True, False])
result_true_array1 = np.array([1, 2])
result_false_array2 = np.array([100, 200])
print np.where(condition, result_true_array1,result_false_array2)


factor_data = '\n6.23,5.34,7.23,3.65\n'
print factor_data.strip().split(',')  # strip:去除首尾给定字条，默认是\t\n等特殊字符
print 'Python\tand\t\tc++'.expandtabs()  #\t ---> tab
print 'python and c++'.replace('python','PYTHON')


'''
Sorting 
.sort_values()
.sort_index()
'''
sort_data = pd.Series(
    [0.01,-0.01, 0.07, 0.05, 0.02, 0.019, -0.019],
    index=['600001', '600002', '600003', '600004', '600005', '600006', '600007']
)
def sort_change(return_date):
    sorted_date = return_date.sort_values(ascending=True)
    return list(sort_data.index[:10])
def sort_index_change(return_date):
    sorted_date = return_date.sort_index(ascending=False)
    return list(sort_data.index[:10])
print sort_change(sort_data)
print sort_index_change(sort_data)

df = pd.DataFrame(
    [1,2,3,4],
    index=['a','c','d','b'],
    columns=['col']
)
print df.sort_index()


#Dictionary
factor_data = {'600001':10, '600002':-5, '600000':0, '600004':-1, '600005':3, '600006':5}
####实现1
chosen_data = [key_in_dict for key_in_dict in factor_data if factor_data[key_in_dict] > 0]
print chosen_data
####实现2 Dict 转成 Series
factor_data_series = pd.Series(factor_data)
chosen_data = list(factor_data_series[factor_data_series>0].index)
for key_in_dict in factor_data:
    print key_in_dict, ' ::: ', factor_data[key_in_dict]


#Matplot 画图
'''
plt.plot    折线图
plt.bar     条形图
plt.scatter 散点图
plt.hist  直方图
plt.pie   饼状图
plt.boxplot 箱形图
'''
import matplotlib.pyplot as plt
data_textile = pd.Series(
    {'2018/01/02':7.74, '2018/01/03':7.88, '2018/01/04':8.12,
     '2018/01/05':7.92, '2018/01/08':7.95, '2018/01/09':7.9,
     '2018/01/10':7.82, '2018/01/11':7.81, '2018/01/12':7.74,
     '2018/01/15':7.56},
)
data_textile.index = pd.to_datetime(data_textile.index)
data_clothing = pd.Series(
    {'2018/01/02':9.81, '2018/01/03':9.88, '2018/01/04':9.12,
     '2018/01/05':9.92, '2018/01/08':9.95, '2018/01/09':9.9,
     '2018/01/10':9.82, '2018/01/11':9.81, '2018/01/12':9.74,
     '2018/01/15':9.56},
)
data_clothing.index = pd.to_datetime(data_clothing.index)
print data_clothing
print data_textile
plt.figure(figsize=(10,6))   #图的大小
plt.plot(data_textile,'ro-',label='stock in Textile industry')
plt.plot(data_clothing,'bo-', label ='stock in Clothing industry')
plt.legend()
plt.xticks(rotation=45)
plt.title('2 stocks')
plt.grid()
plt.ylim(7, 15)  #y轴坐标上下限值
plt.show()
#correlation
print data_textile.corr(data_clothing)


###Classes
class Position():
    def __init__(self):
        self._trade_records = []
    def add_record(self,trade):
        self._trade_records.append(trade)
position_instance = Position()
position_instance.add_record(('60001',600,'2018-01-01'))
print position_instance._trade_records

#Groupby in DataFrame
df = pd.DataFrame(
    [['industry1', 30, 0.05],
     ['industry1', 15, 0.07],
     ['industry2', 5, -0.01],
     ['industry1', 20, 0.1],
     ['industry2', 8, 0.03]],
    index=['stock1','stock2','stock3','stock4','stock5'],
    columns=['industry','PE','ROE']
)
pe_max = df.groupby('industry').apply(lambda df:df['PE'].max())
pe_max2 = df.groupby('industry')['PE'].max()
pe_max3 = df.groupby('industry').max()['PE']
roe_min = df.groupby('industry').apply(lambda df:df['ROE'].min())
print pe_max


df = pd.DataFrame(
    np.random.randn(100),
    index=pd.date_range('2018-01-01',periods=100),
    columns=['close']
)
df['change'] = df['close'].pct_change()
std = df['change'].std()
monthly_change = (df['change']+1).resample('M').prod() -1
sharpe_ratio=(df['change'].mean() - 0.04/252) / std  #资产的按日算的夏普比率sharpe ratio



#DataFrame loc iloc
df = pd.DataFrame(
    [[12.34, 1.56, 6.91, 3032.25, 0.02],
     [6.75, 1.05, 6.91, 32.25, 0.2],
     [2.34, 1.6, 6.91, 2032.25, 0.12],
     [3.35, 2.56, 6.91, 8032.25, 0.22],
     [16.74, 5.56, 6.91, 5032.25, 0.32],
     [1.34, 1.3, 7.91, 1032.25, 0.42]
     ],
    index=['600100','600102','600103','600104','600105','600106'],
    columns=['VOLATILITY', 'LIQUIDITY', 'PE', 'SIZE', 'LEVERAGE']
)
print df.iloc[1:4, [3,4]]
print df.loc['600100':'600103',['SIZE','LIQUIDITY']]
print df['SIZE']
print df.loc['600100']
print df.loc['600100':'600103']
print df['600100':'600103']
print df.iloc[:, 0:4]


#Numpy np array
roe_data = np.array([0.02, 0.12, 0.20, 0.13, -0.04, 0.05, 0.15, 0.07, 0.18, 0.05])
print roe_data[roe_data > 0.06]
print roe_data > 0.06


#fillna bfill ffill
raw_data = pd.Series([4.55, 4.67, 4.88, 4.73, np.nan, np.nan, 4.35, 4.13, 3.99, 3.76, 3.75])
raw_data_adjust = raw_data.fillna(value=raw_data.mean())
raw_data_adjust = raw_data.fillna(method='ffill')
raw_data_adjust = raw_data.fillna(method='bfill')
raw_data_adjust = raw_data.interpolate()  #线性插值
#raw_data.isna()
#raw_data.notna()


#改变采样频率 resample  1d -> 3d, 并计算3天的累计收益   W, M , Q, A/Y, H, T/min, S
df = pd.DataFrame(
    [0.00565, 0.063777, -0.030280, -0.028017, 0.039533, 0.033460, -0.043319],
    index = [pd.date_range('2018-01-01', periods=7)],
    columns= ['daily_return']
)
print df['daily_return'].resample('3d').apply(lambda df: (df+1).prod() - 1)


'''
CAPM模型：资产收益率与市场组合收益率之间的关系，相当于单因子模型
APT模型：认为市场组合并不是影响资产收益率的唯一因素，使用多种因素解释资产收益率，相当于多因子模型
ARIMA模型：自回归移动平均模型，时间序列预测模型
DDM模型：股利贴现模型，公怀估值常用模型
GARCH模型：自回归条件异方差模型，时间序列预测模型
Black-Scholes模型：期权定价模型
VaR模型： 风险控制模型
'''


'''
Jupyter Notebook Magic Commands 魔法命令
%who
%time
%lsmagic  #显示所有魔法命令
%pwd
%debug
'''


stock_data = np.array([
                      [0.02, 0.04, 0.01, -0.02, 0.03],
                      [0.1, 0.1, 0.08, -0.01, -0.02],
                      [0.01, 0.02, 0, -0.01, -0.01]
                       ])
print np.std(stock_data, axis=1)  #按行， 3行， 3个值结果
print np.std(stock_data, axis=0)  #按列， 5列， 5个值结果
'''
np.mean()
np.var()  #方差
np.average()
'''

#面向对象
'''
1.类属性可以被所有实例访问
2.类私有属性不能直接访问
3.实例的属性无法用类名访问
'''
class Instrument(object):
    name = 'EURUSD'      #### 类属性
    __type = 'currenty'  #### 类属性 （private 私有属性）
c = Instrument()
c.exchange = 'ICE'       ### 实例属性
print Instrument.name
print Instrument._Instrument__type
#print c.__type


'''
机器学习：
1.逻辑回归
2.决策树
3.KNN  
4.神经网络
'''



