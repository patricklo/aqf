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
