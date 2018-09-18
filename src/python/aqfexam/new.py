# -*- coding: UTF-8 -*-
import pandas as pd

return_data = pd.DataFrame(
    {'stock_1':[0.01, 0.03, 0.02, 0.01, 0.05, -0.10, -0.05,-0.01, 0.01, 0.01, 0.02, 0.01],
     'stock_2':[-0.01, -0.02, 0.02, 0.01, 0.02, 0.03, 0.02, 0.05, 0.06, 0.04, 0.05, 0.07],
     'stock_3':[0.01, -0.01, 0.00, 0.01, 0.02, 0.01, -0.02, 0.00, 0.01, 0.03, -0.01, 0.00]},
    index=['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04', '2018-01-05', '2018-01-08',
           '2018-01-09', '2018-01-10', '2018-01-11','2018-01-12', '2018-01-15', '2018-01-16']
)
return_data.index = pd.to_datetime(return_data.index)
stock_1_return =  return_data['stock_1'].resample('6d').apply(lambda df: (df+1).prod() - 1)
stock_2_return =  return_data['stock_2'].resample('6d').apply(lambda df: (df+1).prod() - 1)
stock_3_return =  return_data['stock_3'].resample('6d').apply(lambda df: (df+1).prod() - 1)

df = pd.DataFrame(
    [0.00565, 0.063777, -0.030280, -0.028017, 0.039533, 0.033460, -0.043319],
    index = [pd.date_range('2018-01-01', periods=7)],
    columns= ['daily_return']
)
print df['daily_return']
print df['daily_return'].resample('3d').apply(lambda df: (df+1).prod() - 1)

