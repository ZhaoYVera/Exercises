import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

datain = pd.read_excel('2019.11.1-2020.7.14进场.xlsx', header=4, usecols=['箱属', '进场日期', '好坏箱', '堆场', '箱尺', '进场性质'])

datain_cos = datain[(datain['箱属'] == 'COS') & (datain['堆场'] == '1堆场') &
                    (datain['箱尺'] == '22G1') & (datain['进场日期'] > pd.Timestamp('2020-03-07'))]


def get_week_number(dt: pd.Timestamp):
    """get year, week number and day of a Timestamp object"""
    year = dt.year
    month = dt.month
    week_num = int(dt.strftime('%V'))
    day = (dt - pd.Timestamp('1994-06-20')).days % 7 + 1
    if month == 12 and week_num == 1:
        return year+1, week_num, day
    return year, week_num, day


# func1 = lambda x: x.strftime('%V')
# datain_cos_1['周数'] = datain_cos_1['进场日期'].map(func1)
# func2 = lambda x: (x-pd.Timestamp('2020-01-06')).days % 7 + 1
# datain_cos_1['周几'] = datain_cos_1['进场日期'].map(func2)
new_data = datain_cos['进场日期'].map(get_week_number)
datain_cos[['年份', '周数', '周几']] = new_data.apply(pd.Series)

datain_cos_1 = datain_cos[(datain_cos['进场日期'] > pd.Timestamp('2020-01-05')) &
                          (datain_cos['进场日期'] < pd.Timestamp('2020-07-13'))]

datain_cos_1_new = datain_cos_1[datain_cos_1['周数'] > 10]

qweek = datain_cos_1_new['周数'].value_counts()
# plt.plot(qweek.sort_index())
# plt.show()

datain_week = defaultdict(int)
for item in datain_cos_1_new.iloc:
    datain_week[(item['周数'], item['周几'])] += 1

qday = datain_cos['进场日期'].value_counts().sort_index()
qday = pd.DataFrame(qday)
# qday.loc[pd.Timestamp('2020-03-07')] = np.nan
# qday.loc[pd.Timestamp('2020-07-15')] = np.nan
qday['3日平均'] = np.nan
for dt in qday.index:
    if dt > pd.Timestamp('2020-03-08') and dt < pd.Timestamp('2020-07-14'):
        qday.loc[dt, '3日平均'] = (qday.loc[dt-pd.Timedelta('1 days'), '进场日期'] +
                                qday.loc[dt, '进场日期'] + qday.loc[dt+pd.Timedelta('1 days'), '进场日期'])/3
qday = qday.dropna().reset_index()
qday.columns = ['进场日期', '数量', '3日平均']
qday[['年份', '周数', '周几']] = qday['进场日期'].map(get_week_number).apply(pd.Series)[:-1]

distribution_3d = defaultdict(float)
for week, day in datain_week.keys():
    distribution_3d[(week, day)] = datain_week[(week, day)]/qweek.loc[week]
distribution_week_3d = pd.Series(distribution_3d, index=distribution_3d.keys())
distribution_week_3d = distribution_week_3d.unstack()
distribution_week_3d.columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                                'Friday', 'Saturday', 'Sunday']
distribution_week_3d.plot()
plt.show()

distribution = defaultdict(float)
for week, day in datain_week.keys():
    distribution[(week, day)] = datain_week[(week, day)]/qweek.loc[week]

distribution_week = pd.Series(distribution, index=distribution.keys())
distribution_week = distribution_week.unstack()
distribution_week.columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                             'Friday', 'Saturday', 'Sunday']
# distribution_week.plot()
