# -*- coding: UTF-8 -*-
import pandas as pd

score_data = pd.Series(
    [100,-0.01, 0.07, 0.05, 0.02, 0.019, 999],
    index=['600001', '600002', '600003', '600004', '600005', '600006', '600007']
)

chosen_stock_codes = list(score_data.sort_values(ascending=False).index[:10])
print chosen_stock_codes
