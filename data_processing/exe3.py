import pandas as pd
import seaborn as sns

datain = pd.read_excel('2019.11.1-2020.7.14进场.xlsx', header=4,
                       usecols=['箱号', '箱属', '箱尺', '进场日期', '进场时间', '好坏箱',
                                '当前好坏箱', '堆场', '区', '位', '进场准备时间'])[:-5]
dataout = pd.read_excel('2019.11.1-2020.7.14出场.xlsx', header=4,
                        usecols=['箱号', '箱属', '箱尺', '出场日期', '出场时间', '堆存天数', '当前好坏箱',
                                 '堆场', '区', '位', '列', '层', '出场准备时间', '车载确认时间'])[:-5]
# datarep = pd.read_excel('20191215-20191221-修箱报表.xlsx', header=4, usecols=['箱号', '状态日期', '堆场'])

damage_distribution_month = datain[['箱属', '箱尺', '进场日期', '好坏箱']]
damage_distribution_month['进场年月'] = damage_distribution_month['进场日期'].dt.month
damage_distribution_month_cos = damage_distribution_month[damage_distribution_month['箱属'] == 'COS']
sns.barplot(damage_distribution_month_cos)
# data16in = datain[(datain['进场日期'] == pd.Timestamp('2019-12-16 00:00:00')) & (datain['堆场'] == '1堆场')]
# data16out = dataout[(dataout['出场日期'] == pd.Timestamp('2019-12-16 00:00:00')) & (dataout['堆场'] == '1堆场')]
# data16inout = pd.merge(data16in, data16out, on='箱号')
# data16rep = datarep[(datarep['状态日期'] == pd.Timestamp('2019-12-16 00:00:00')) & (datarep['堆场'] == '1堆场')]
