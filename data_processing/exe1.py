import pandas as pd

# data = pd.read_excel('orderTemplate.xlsm')
data = pd.read_csv('orderTemplate.csv', header=1, index_col=9)
new_data = pd.read_excel('itemTemplate.xlsx', sheet_name='sheet0', header=1, index_col=0, usecols=[0, 3, 4, 5])

result = pd.merge(data, new_data, left_on='料箱代码(必填项)', right_index=True, how='left', sort=False)

result.to_csv('newOrderTemplate.csv', index=True, header=True)
