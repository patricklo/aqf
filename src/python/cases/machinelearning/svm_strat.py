# coding:utf-8
from pylab import plt
import seaborn
from matplotlib import mpl

import pandas as pd
import numpy as np
import tushare as ts


hs300  = ts.get_k_data('hs300', start='2013-01-01', end='2016-06-25')  ##训练集数据  features_trained
hs300.set_index('date', inplace=True)
hs300['returns'] = hs300['close'].pct_change()
hs300.dropna(inplace=True)

'''
1. 数据的处理： 特征工程处理
'''

for i in range(1, 8, 1): #1到8， steps步进：1
    hs300['close-'+str(i)+'d'] = hs300['close'].shift(i)  # 一共到前8天的close_price, 8个特征

hs_7d = hs300[[x for x in hs300.columns if 'close' in x]].iloc[7:]
import sklearn
from sklearn import linear_model
x_train_features = hs_7d
'''
对feature（即因子） 进行标准化，因为在实际用途中，不同的feature含义不一样
（本例中因所有feature都是价格，所以不标准化也是一样效果）
'''
x_train_features = sklearn.preprocessing.scale(x_train_features) #对feature特征标准化？？   #### x_train => features_trained
#### x_train => feature_trained



'''
2.逻辑回归算法实现    features_trained and label_trained
'''

####y_train => lable_trained
lm = linear_model.LogisticRegression(C=1000)
'''
### C=1000 => tradeoff 光滑的决策边界 和 正确分类所有训练点/ 正则化的力度  =》防止过度拟合   C越小，、、、

1.C越大，模型越精确
2.c tradeoff是定义对决策边界的光滑度，一般C越大，说明决策边界越不光滑，但模型越准确
'''
y_train_label = np.sign(hs_7d['close'].pct_change().shift(-1))  #### label_trained
y_train_label.replace(to_replace=np.NAN, value=0, inplace=True)
y_train_label = y_train_label.reshape(-1,1 )  ####  reshape => 移除日期索引 ， 只返回一个array

lm.fit(x_train_features, y_train_label)
print lm.score(x_train_features, y_train_label)  ####accuracy_score一样，也是对训练feature和给定 label进行对比 打分，看准确度。  此例中是给训练features 对比 给定训练集的label  ， 不是对测试集的Label对比
'''lm.score 
和
accuracy_score一样，也是对训练feature和给定 label进行对比 打分，看准确度。  此例中是给训练features 对比 给定训练集的label  ， 不是对测试集的Label对比 
'''

hs300['predict'] = np.NaN
hs300['predict'].ix[7:] = lm.predict(x_train_features)
hs300['predict'] = hs300['predict'].shift(1)

hs300['strats_returns'] = (hs300['predict'] * hs300['returns'] + 1).cumprod()  ##策略累计收益
hs300['cum_ret'] = (hs300['returns']+1).cumprod() ##实际收益


#hs300[['strats_returns','cum_ret']].dropna().plot(figsize=(10,6))
#plt.show()


'''
2.1 改为SVM算法实现

'''
from sklearn.svm import SVC
clf_SVC = SVC(kernel='linear')
clf_SVC.fit(x_train_features,y_train_label)
print 'SVC score='+str(clf_SVC.score(x_train_features,y_train_label))

hs300['SVC_predict'] = np.NaN
hs300['SVC_predict'].ix[7:] = clf_SVC.predict(x_train_features)
hs300['SVC_predict'] = hs300['SVC_predict'].shift(1)

hs300['SVC_strats_returns'] = (hs300['SVC_predict'] * hs300['returns'] + 1).cumprod()  ##策略累计收益
hs300['cum_ret'] = (hs300['returns']+1).cumprod() ##实际收益

#hs300[['SVC_strats_returns','cum_ret']].dropna().plot(figsize=(10,6))
#plt.show()

'''
3. 用逻辑回归算法对测试集的验证 features_test
'''

hs300_test = ts.get_k_data('hs300', start= '2016-07-01', end='2017-06-30')
hs300_test.set_index('date', inplace=True)
hs300_test['returns'] = hs300_test['close'].pct_change()
hs300_test.dropna(inplace=True)

for i in range(1, 8 ,1):
    hs300_test['close -'+str(i)+'d'] = hs300_test['close'].shift(i)

hs_7d_test = hs300_test[[x for x in hs300_test.columns if 'close' in x]].iloc[7:]  #只拿和close有关的列做为features 因子

x_test_features = hs_7d_test
x_test_features = sklearn.preprocessing.scale(x_test_features)

hs300_test['predict'] = np.NaN
x_test_label = lm.predict(x_test_features)

hs300_test['predict'].ix[7:] = x_test_label
hs300_test['predict'] = hs300_test['predict'].shift(1)

hs300_test['strats_returns'] = (hs300_test['predict'] * hs300_test['returns'] + 1).cumprod()  ##策略累计收益
hs300_test['cum_ret'] = (hs300_test['returns']+1).cumprod() ##实际收益

#hs300_test[['strats_returns','cum_ret']].dropna().plot(figsize=(10,6))
#plt.show()


'''
3.1 用SVM算法对测试集的验证 features_test
'''
x_test_features = hs_7d_test
x_test_features = sklearn.preprocessing.scale(x_test_features)

hs300_test['predict'] = np.NaN
x_test_label = clf_SVC.predict(x_test_features)

hs300_test['predict'].ix[7:] = x_test_label
hs300_test['predict'] = hs300_test['predict'].shift(1)

hs300_test['strats_returns'] = (hs300_test['predict'] * hs300_test['returns'] + 1).cumprod()  ##策略累计收益
hs300_test['cum_ret'] = (hs300_test['returns']+1).cumprod() ##实际收益

hs300_test[['strats_returns','cum_ret']].dropna().plot(figsize=(10,6))
plt.show()

