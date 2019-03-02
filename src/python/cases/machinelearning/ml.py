# coding:utf-8

'''
机器学习分类：
 1.监督学习： 特征，标签
 2.无监督学习： 训练样本中无标签或特征等属性，如聚类问题等



欠拟合:  high bias
过拟合： high variance -> 验证集
        原因：解释因子太多了
       解决方法：线性 =》 正则化 =》 引入惩罚因子

'''
import matplotlib.pyplot as plt
from visualization import plot_pic
from produce_data import produce_data
import numpy as np

data = produce_data()


print data.head()

#准备训练集，测试训练集
##from sklearn.cross_validation import train_test_split
from sklearn.model_selection import  train_test_split
##test_size:0.25 25%算测试集， 75%是训练集
features_train, features_test, label_train, label_test = train_test_split(data[['practice','time_period']], data['label'], test_size=0.25)

train_data = features_train.copy()
train_data['label'] = label_train

print 'test'

practice_fail = train_data[train_data['label'] == 0]['practice']
time_period_fail = train_data[train_data['label'] == 0]['time_period']

practice_pass=train_data[train_data['label'] == 1]['practice']
time_period_pass = train_data[train_data['label'] == 1]['time_period']

plt.figure(figsize=(6,6))
plt.xlim(0.0,1.0)
plt.ylim(0.0, 1.0)
plt.scatter(practice_fail, time_period_fail, color='b', label='fail')
plt.scatter(practice_pass, time_period_pass, color='r', label='pass')
plt.xlabel('practice')
plt.ylabel('time_period')
plt.legend(loc='upper right')
plt.show()
