#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore') #忽略警告信息
import tushare as ts

#解决中文标题显示问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


'''
本代码对应 -> 18. 量化投资与技术分析_5.形态识别和移动止损策略_2.锤子线形态识别

锤子线/上吊线 特征：
K线中， 实体线为中间长方形部分， 上影线为实体上方的直线部分， 下影线为实体下方的直线部分
（上涨： 红色， 实体上边界为收盘价，下边界为开盘价，上影线为当天最高价，下影线为当天最低价
  下跌： 绿色，实体上边界为开盘价，下边界为收盘价，上影线为当天最高价，下影线为当天最低价）
1. 中间实体小
2. 上影线短
3. 下影线长 （一般大于中间实体线3倍以上）




'''