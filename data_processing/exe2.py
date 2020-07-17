import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data_in = pd.read_excel('20191215-20191221-IN.xlsx', header=4, usecols=['进场时间', '还箱时长', '堆场'])
data1_in = data_in[data_in['堆场'] == '1堆场']
tmp_xin = data1_in['进场时间']
xin = []
for time in tmp_xin:
    xin.append(time.hour)
    # xin.append(time.hour + time.minute/60 + time.second/3600)
yin = data1_in['还箱时长']
avrperhourin = pd.DataFrame(list(yin), xin)
avrperhourin.reset_index(inplace=True)
avrperhourin['inout'] = 'IN'
avrperhour_dict = {}
for i in range(24):
    avrperhour_dict[i] = [avrperhourin[avrperhourin['index'] == i][0].mean()]

data_out = pd.read_excel('20191215-20191221-OUT.xlsx', header=4, usecols=['出场时间', '堆场', '提箱时长'])
data1_out = data_out[(data_out['堆场'] == '1堆场') & (data_out['提箱时长'] < 60)]
tmp_xout = data1_out['出场时间']
xout = []
for time in tmp_xout:
    xout.append(time.hour)
    # xout.append(time.hour + time.minute/60 + time.second/3600)
yout = data1_out['提箱时长']
avrperhourout = pd.DataFrame(list(yout), xout)
avrperhourout.reset_index(inplace=True)
avrperhourout['inout'] = 'OUT'
for i in range(24):
    avrperhour_dict[i].append(avrperhourout[avrperhourout['index'] == i][0].mean())
#
# result = pd.DataFrame(avrperhour_dict, index=['IN', 'OUT']).T
# result.reset_index(inplace=True)

sns.barplot(hue='inout', x='index', y=0, data=pd.concat([avrperhourin, avrperhourout], axis=0))
# sns.barplot(x='index', y='OUT', data=result, color=(0, 0, 0.9))
# pd.DataFrame(avrperhour_dict).plot.bar()
plt.show()

# xin.extend(xout)
# y = yin.append(yout)
# plt.scatter(xin, yin, s=5, edgecolors='blue')
# plt.scatter(xout, yout, s=5, edgecolors='red')
# plt.title('1duichang')
# plt.xlabel('shijian')
# plt.ylabel('shichang')
# plt.show()

# plt.hist(avrperhour_dict.values())
# plt.plot(list(avrperhour_dict.values()))
# avrperhour.plot(kind='hist')
# avrperhourin.plot(kind='bar')
# avrperhour.plot(kind='bar')
# result.plot(kind='bar')
# plt.hist2d(xin, yin, density=True)
# plt.show()
