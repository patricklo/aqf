#coding:utf-8
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter('ignore')

df = pd.Series(range(10, 20))
print df

print df.values
print type(df.values)

print df.head(5)

print '###############################'
print '###通过字典构造Series############'
print '###############################'
sales_data = {'a': 1, 'b': 2, 'c': 3}
df = pd.Series(sales_data)

df.name = 'Series1'
df.index.name = 'Series1_Index'
print df.head()
print df.index
print df.values


df = pd.Series(range(8, 14), index=['a', 'b', 'c','d', 'e', 'f'])
print df[1] #通过Position去选择
print df['b'] #通过index去选择

print '#####切片选择:连续'
print df['b':'d'] #切片选择:连续
print '#####切片选择:不连续'
print df[['a','d']] #切片选择： 不连续




print '###############################'
print '#########Pandas DataFrame的构建#######'
print '###############################'

print '####通过random随机数构造Pandas DataFrame'
arrayrdn = np.random.randn(6,4)
print arrayrdn

df = pd.DataFrame(arrayrdn)
print df

df = pd.DataFrame(np.random.randn(6,4), columns={'a','b','c','d'}, index=['e','f','g','h','i','j'])
print df #给定index和columns名字
print df.head


print '##通过字典构造Pandas DataFrame'
dict_data = {'Date': pd.Timestamp('20170630'),
             'Number':pd.Series(6, index=list(range(4))),
             'Course_name':pd.Series(["Python","Java","C++","Scala"]),
             'Company':'PATRICK Limted'
             }
df = pd.DataFrame(dict_data)

print df.head()


print '####自定义构建Pandas DataFrame'
data_np = np.array([[10, 30, 60, 80],['Math','Eng', 'Chem', 'History']])

print data_np.transpose()

df = pd.DataFrame(data_np.transpose())
print df
print type(df.values)


print '###############################'
print '#########Pandas DataFrame的选择操作#######'
print '###############################'

df = pd.DataFrame(np.random.randn(6,4), columns={'a','b','c','d'}, index=['e','f','g','h','i','j'])

print df.loc[['f','h'],['b']]  #loc 只能针对index进行访问
print df.iloc[1:4]    # 通过Position访问

#print df.ix   #混合索引 ---->   新版本已取消



dict_data = {'Date': pd.datetime(2017,11,26),
             'Number': pd.Series([6,6,6,6]),
             'Course_name': pd.Series(['PYthon','Quant', 'Java', 'Analyst']),
             'Company' : 'Patrick.co ltd'}
df = pd.DataFrame(dict_data)

print df

df['Period'] = range(21,25
                     )
print df

del(df['Period'])
print df

df['ROE'] = range(21,25)
print df
print df.head()


df = pd.DataFrame([80.5, 90, 58, 88],
                  columns=['Scores'],
                  index=['a', 'b', 'c', 'd'],
                  dtype='f')

df['Hours'] = (2.1, 1.5, 1.6, 2.2)


df['Names'] = pd.DataFrame(['Alpha','Beta', 'Gamma', 'Theta'],
                           index = ['d', 'b', 'a', 'c'])  #index 可以打乱顺序，顺序无关

print df


print '#####  DataFrame 对齐操作  ###########'

df1 = pd.DataFrame(np.random.random((6, 6)),
                   columns=['a', 'b', 'c', 'd', 'e', 'f'])
df2 = pd.DataFrame(np.random.random((3, 3)),
                   columns=['a', 'b', 'c'])

df3 = df1 + df2  #自动对齐，没有值对应NaN


print df3

df3.fillna(1, inplace=True)   #NaN空值赋值

print df3

print '####### 按条件筛选， 条件选股  ################'
index_all = ['Comp A', 'Com B', 'Com C ', 'Com d']
d = {'PE': pd.Series([10., 20., 30, 40], index=index_all),
    'PB' : pd.Series([2., 3., 2.5, 4.], index=index_all),
    'ROE' : pd.Series([0.06, 0.1, 0.08, 0.02], index=index_all)}

df = pd.DataFrame(d)
print df

print '##### PE<25 #####'
print (df.PE < 25)

print (df['PE'] < 25)

print df[df.PE < 25]

print '##### 多条件组合  ######'
print (df.PE < 25)*1  #作用：

print df[(df.PE < 25) & (df.PB < 2.5)] #多条件中， 每个条件需要加括号
#多条件中， 使用& 或者 | 符号

print '####   三个条件满足任意两个   ######'
print ((df.PE < 25) * 1 + (df.PB < 2.5) * 1 + (df.ROE > 0.07)) == 2
print df[(df.PE < 25) * 1 + (df.PB < 2.5) * 1 + (df.ROE > 0.07) * 1 ==2]  #三个条件满足任意两个


print '########### DataFrame Apply 函数的重点应用   #########################'
print '################################'

a = np.random.randn(9, 6)

print a.round(5)  # rounding 5位小数点

df = pd.DataFrame(a)
print df

df.columns = ['a', 'b', 'c', 'd', 'e', 'f']
dates = pd.date_range('2017-1-1', periods=9, freq='M')
df.index = dates
print df

def squqre_fun(x):
    return x**2

print df.apply(squqre_fun)   #所有数据开平方

print df.apply(lambda x: x ** 2)  #同上，使用Lambda方式

def find_min(x):
    return x.min()

print df.apply(find_min)  #每列的最小值

#每行的最小值
print df.apply(find_min, axis=1)

print '##########  DataFrame 排序   ###########'
print df.sort_index(ascending=False)

print df.sort_index(axis=1, ascending=False)

print df.sort_values(by='b')


print '###### DataFrame 通用函数应用   #########'
print df.sum()
print df.sum(axis = 1)

print df.mean()

print df
print '######## df.comsum  #########'
print df.cumsum

print df.describe()


print '########## DataFrame 空值处理   ##########'

print np.sqrt(df)

print np.sqrt(df).sum()

df_nan = pd.DataFrame([np.random.randn(4), [1.5, np.nan, np.nan, 5],
                       [4.5, np.nan, np.nan, np.nan],[1.5, np.nan, 2.5, np.nan]])
print df_nan.head()

print df_nan.isnull()


print df_nan.dropna(axis=0)

print df_nan.dropna(axis=1)

print df_nan.fillna(0)

print df.iloc[:, 1]
print df.loc[:,'b']











