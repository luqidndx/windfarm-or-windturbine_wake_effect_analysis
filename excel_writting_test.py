# -*- coding: utf-8 -*-
"""
@author: luqi
@Created on
@instruction：
@Version update log:
"""

import pandas as pd

# create some Pandas DateFrame from some data
df1 = pd.DataFrame({'Data1': [1, 2, 3, 4, 5, 6, 7]})
df2 = pd.DataFrame({'Data2': [8, 9, 10, 11, 12, 13]})
df3 = pd.DataFrame({'Data3': [14, 15, 16, 17, 18]})
All = [df1, df2, df3]
# create a Pandas Excel writer using xlswriter
writer = pd.ExcelWriter('test.xlsx')

df1.to_excel(writer, sheet_name='Data1', startcol=0, index=False)
df2.to_excel(writer, sheet_name='Data1', startcol=1, index=False)
writer.close()
