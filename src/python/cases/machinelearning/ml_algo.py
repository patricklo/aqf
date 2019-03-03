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

'''
features_trained: 已分类好的feature数据
label_trained：   已分类好的feature数据的label数据

features_test：待验证的feature数据 
label_test： 待验证的feature数据的实现label数据， 用于之后对比算法计算出来的label数据（如后面：clf_DT,clf_LR等）

'''
features_trained, features_test, label_trained, label_test = train_test_split(data[['practice','time_period']], data['label'], test_size=0.25)



'''
1.逻辑回归算法实现
'''

# from sklearn.linear_model import LogisticRegression
# clf_LR= LogisticRegression()
# clf_LR.fit(features_train,label_train)
#
# predict_label_test_LR = clf_LR.predict(features_test)
# plot_pic(clf_LR, features_test, label_test)#传入已学习好的分类器、测试标签和测试标签的label，画出分类器predict的决策边界和标签的实际点状图，可以得知分类准确不准确
#
# from sklearn.metrics import accuracy_score
# acc=accuracy_score(predict_label_test_LR, label_test)  #准确率
#
# print acc


'''
2. 决策树算法实现
'''
# from sklearn.tree import DecisionTreeClassifier
#
# clf_DT = DecisionTreeClassifier()
# clf_DT.fit(features_train,label_train)
#
# predict_label_test_DT = clf_DT.predict(features_test)
# plot_pic(clf_DT, features_test, label_test)#传入已学习好的分类器、测试标签和测试标签的label，画出分类器predict的决策边界和标签的实际点状图，可以得知分类准确不准确
#
# from sklearn.metrics import accuracy_score
# acc=accuracy_score(predict_label_test_DT, label_test)  #准确率
#
# print acc


'''
2.1. 随机森林算法实现
'''
# from sklearn.ensemble import RandomForestClassifier
#
# clf_RFC = RandomForestClassifier()
# clf_RFC.fit(features_train,label_train)
#
# predict_label_test_RFC = clf_RFC.predict(features_test)
# plot_pic(clf_RFC, features_test, label_test)#传入已学习好的分类器、测试标签和测试标签的label，画出分类器predict的决策边界和标签的实际点状图，可以得知分类准确不准确
#
# from sklearn.metrics import accuracy_score
# acc=accuracy_score(predict_label_test_RFC, label_test)  #准确率
#
# print acc

'''
3. KNN 算法实现
'''
#
# from sklearn.neighbors import KNeighborsClassifier
# clf_KNN = KNeighborsClassifier(n_neighbors=5)
# clf_KNN.fit(features_trained, label_trained)
#
# predict_label_test_KNN = clf_KNN.predict(features_test)
# plot_pic(clf_KNN, features_test,label_test)

'''
4. 朴素贝叶斯(naive_bayes)算法实现:

bayes贝叶斯公式:AB同时发生的概率  P(AB) = P(A) * P(B|A) = P(B) * P(A|B) 
'''

# from sklearn.naive_bayes import GaussianNB
#
# clf_NB = GaussianNB()
# clf_NB.fit(features_trained, label_trained)
#
# predict_label_test_NB = clf_NB.predict(features_test)
# plot_pic(clf_NB, features_test, label_test)


'''
5. SVM支持向量机算法

  SVC: 分类问题
  SVR：回归问题
'''
from sklearn.svm import SVC
# clf_SVC = SVC()
# clf_SVC.fit(features_trained,label_trained)
#
# predict_label_test_SVC = clf_SVC.predict(features_test)
# plot_pic(clf_SVC, features_test, label_test)

clf_SVC2 = SVC(kernel='rbf') ### Kernel: SVC - rbf : 高斯核   默认的， 不给定也行
###gamma=auto是默认 需要人为经验去定义 ， 可指定 数字， 控制 SVM中点到决策边界的距离大小的影响权重， gamma越大,代表到决策边界最近的点的权重越大
#clf_SVC2 = SVC(kernel='rbf', gamma=1000)
clf_SVC2.fit(features_trained,label_trained)

predict_label_test_SVC = clf_SVC2.predict(features_test)
plot_pic(clf_SVC2, features_test, label_test)
