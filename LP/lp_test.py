import pulp as plp

names_shuiku = ['A', 'B', 'C']
names_xiaoqv = ['jia', 'yi', 'bing', 'ding']
max_quantity = {'A': 50, 'B': 60, 'C': 50}
xiaoqv_basic = {'jia': 30, 'yi': 70, 'bing': 10, 'ding': 10}
xiaoqv_extra = {'jia': 50, 'yi': 70, 'bing': 20, 'ding': 40}

management_fee = {'A': {'jia': 160, 'yi': 130, 'bing': 220, 'ding': 170},
                  'B': {'jia': 140, 'yi': 130, 'bing': 190, 'ding': 150},
                  'C': {'jia': 190, 'yi': 200, 'bing': 230, 'ding': 9999}}

supply = plp.LpProblem(name='The water delivery problem', sense=plp.LpMaximize)
xx = plp.LpVariable.dicts(name='water',
                          indexs=[(shuiku, xiaoqv) for shuiku in names_shuiku for xiaoqv in names_xiaoqv],
                          lowBound=0)

for shuiku in names_shuiku:
    supply += plp.lpSum([xx[(shuiku, xiaoqv)] for xiaoqv in names_xiaoqv]) <= max_quantity[shuiku]

for xiaoqv in names_xiaoqv:
    supply += plp.lpSum([xx[(shuiku, xiaoqv)] for shuiku in names_shuiku]) >= xiaoqv_basic[xiaoqv]
    supply += plp.lpSum([xx[(shuiku, xiaoqv)]
                         for shuiku in names_shuiku]) <= xiaoqv_basic[xiaoqv] + xiaoqv_extra[xiaoqv]

supply += plp.lpSum((450-management_fee[shuiku][xiaoqv])*xx[(shuiku, xiaoqv)] for shuiku in names_shuiku
                    for xiaoqv in names_xiaoqv)

status = supply.solve()
print(supply)
print(plp.LpStatus[status])  # whether solved or not
print(plp.value(supply.objective))  # result
for v in supply.variables():  # values of variables
    print(v.name, ' = ', v.varValue)
