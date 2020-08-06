import json
import pulp as plp
# from .linearprogramming import Simplex

with open('RouteResult2.json', 'r', encoding='utf-8') as f:
    cats = json.loads(f.read())

cats_dalian = cats['Route辽宁大连']
cats_lanzhou = cats['Route甘肃兰州']

cats1 = cats_dalian[0]['pickup']
cats2 = cats_lanzhou[0]['pickup']
# 按照 'volume' 装猫
total_volume1 = sum(dingdan['volume'] for dingdan in cats1)
total_volume2 = sum(dingdan['volume'] for dingdan in cats2)

trucks_names = ['yiweike_5', 'yiweike_4_5', 'yiweike_4_8', 'shangchai_14_5',
                'suofeimu_14', 'suofeimu_18_1', 'suofeimu_13_5',
                'qingling_12_8', 'qingling_12_5', 'qingling_25_87', 'qingling_26_2', 'qingling_24_6',
                'xindongfeng_31', 'dahaowo_52_9', 'xiaohaowo_44_43']
trucks_volumes = {'yiweike_5': 5, 'yiweike_4_5': 4.5, 'yiweike_4_8': 4.8, 'shangchai_14_5': 14.5,
                  'suofeimu_14': 14, 'suofeimu_18_1': 18.1, 'suofeimu_13_5': 13.5,
                  'qingling_12_8': 12.8, 'qingling_12_5': 12.5, 'qingling_25_87': 25.87,
                  'qingling_26_2': 26.2, 'qingling_24_6': 24.6,
                  'xindongfeng_31': 31, 'dahaowo_52_9': 52.9, 'xiaohaowo_44_43': 44.43}
trucks_numbers = {'yiweike_5': 10, 'yiweike_4_5': 5, 'yiweike_4_8': 5, 'shangchai_14_5': 30,
                  'suofeimu_14': 10, 'suofeimu_18_1': 5, 'suofeimu_13_5': 5,
                  'qingling_12_8': 6, 'qingling_12_5': 5, 'qingling_25_87': 1, 'qingling_26_2': 5, 'qingling_24_6': 4,
                  'xindongfeng_31': 10, 'dahaowo_52_9': 5, 'xiaohaowo_44_43': 5}

truck_allocation = plp.LpProblem(name='truck_allocation problem', sense=plp.LpMinimize)
xx = plp.LpVariable.dicts(name='truck', indexs=trucks_names, lowBound=0, cat='Integer')
