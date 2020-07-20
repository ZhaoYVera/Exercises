import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import collections

datain = pd.read_excel('2019.11.1-2020.7.14进场.xlsx', header=4,
                       usecols=['箱号', '箱属', '箱尺', '进场日期', '进场时间', '好坏箱',
                                '当前好坏箱', '堆场', '区', '位', '进场准备时间'])[:-5]
datain = datain[datain['堆场'] == '1堆场']
dataout = pd.read_excel('2019.11.1-2020.7.14出场.xlsx', header=4,
                        usecols=['箱号', '箱属', '箱尺', '出场日期', '出场时间', '堆存天数', '当前好坏箱',
                                 '堆场', '区', '位', '列', '层', '出场准备时间', '车载确认时间'])[:-5]
# datarep = pd.read_excel('20191215-20191221-修箱报表.xlsx', header=4, usecols=['箱号', '状态日期', '堆场'])

damage_distribution = pd.DataFrame(np.arange(60).reshape((30, 2)),
                                   index=[['jan']*5 + ['feb']*5 + ['mar']*5 + ['apr']*5 + ['may']*5 + ['june']*5,
                                          ['COS', 'ONE', 'MSK', 'OOL', 'PIL']*6],
                                   columns=['好箱数', '坏箱数'])
damage_distribution.index.names = ['month', 'corporation']
damage_distribution.columns.names = ['好坏箱']

DMon = {}

damage_distribution_jan = datain[(datain['进场日期'] >= pd.Timestamp('2020-01-01 00:00:00')) &
                                 (datain['进场日期'] < pd.Timestamp('2020-02-01 00:00:00'))]
damage_distribution_feb = datain[(datain['进场日期'] >= pd.Timestamp('2020-02-01 00:00:00')) &
                                 (datain['进场日期'] < pd.Timestamp('2020-03-01 00:00:00'))]
damage_distribution_mar = datain[(datain['进场日期'] >= pd.Timestamp('2020-03-01 00:00:00')) &
                                 (datain['进场日期'] < pd.Timestamp('2020-04-01 00:00:00'))]
damage_distribution_apr = datain[(datain['进场日期'] >= pd.Timestamp('2020-04-01 00:00:00')) &
                                 (datain['进场日期'] < pd.Timestamp('2020-05-01 00:00:00'))]
damage_distribution_may = datain[(datain['进场日期'] >= pd.Timestamp('2020-05-01 00:00:00')) &
                                 (datain['进场日期'] < pd.Timestamp('2020-06-01 00:00:00'))]
damage_distribution_june = datain[(datain['进场日期'] >= pd.Timestamp('2020-06-01 00:00:00')) &
                                  (datain['进场日期'] < pd.Timestamp('2020-07-01 00:00:00'))]

DMon['jan'] = damage_distribution_jan
DMon['feb'] = damage_distribution_feb
DMon['mar'] = damage_distribution_mar
DMon['apr'] = damage_distribution_apr
DMon['may'] = damage_distribution_may
DMon['june'] = damage_distribution_june

for mon, cor in damage_distribution.index:
    damage_distribution.loc[mon, cor] = [len(DMon[mon][(DMon[mon]['箱属'] == cor) &
                                                       (DMon[mon]['好坏箱'] == '好箱')]),
                                         len(DMon[mon][(DMon[mon]['箱属'] == cor) &
                                                       (DMon[mon]['好坏箱'] == '坏箱')])]

# damage_distribution_month = datain[['箱属', '箱尺', '进场日期', '好坏箱']]
# damage_distribution_month['进场年月'] = damage_distribution_month['进场日期'].dt.month
# damage_distribution_month_cos = damage_distribution_month[damage_distribution_month['箱属'] == 'COS']
# sns.barplot(data=damage_distribution_month_cos, hue='好坏箱', x='进场年月')
# plt.show()
# data16in = datain[(datain['进场日期'] == pd.Timestamp('2019-12-16 00:00:00')) & (datain['堆场'] == '1堆场')]
# data16out = dataout[(dataout['出场日期'] == pd.Timestamp('2019-12-16 00:00:00')) & (dataout['堆场'] == '1堆场')]
# data16inout = pd.merge(data16in, data16out, on='箱号')
# data16rep = datarep[(datarep['状态日期'] == pd.Timestamp('2019-12-16 00:00:00')) & (datarep['堆场'] == '1堆场')]
