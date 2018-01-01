#coding:utf-8
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore')
import tushare as ts

'''
pair trading 类别：   ->> 统计套利

1. AH股：价差
2. 内外盘：跨市场
3. 同行业的不同股票
4. ETF

前提：需要cfa 二级知识


思路:
  同行业股票A,B：
  A,B价差的mean， 波动超过一定界限，就认为有套利机会   <----跟mean_reversion策略类似

风险：

   极端变化：某一个公司重大变化，导致价格不再遵守均值回归的规则， 如果说重大发明， 则会引起一个公司的价格一直上涨，别的公司不涨
   
   
前提：
 1. 数据平稳性：stationary   -》要求有点高； 如果数据non-stationary -> （1）拆分 （2） co-integration 协整关系（课程使用的方法）
 2. 
   
'''



