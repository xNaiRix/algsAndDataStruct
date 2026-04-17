f = open("26.txt")
n = int(f.readline())#колво шагов
steps = []
think_to_add = {}
total_think = 0
areas = {}
for line in f.readlines():
    area_id, sub_area_id, think_cnt = map(int, line.split())
    key = (area_id, sub_area_id)
    total_think += think_cnt
    if key not in think_to_add:
        think_to_add[key] = think_cnt
        
    else:
        think_to_add[key] = max(think_to_add[key], think_cnt)
    if area_id not in areas:
        areas[area_id] = think_cnt
    else:
        areas[area_id] += think_cnt
#id самой развитой area (при = кол-ва мыслей выбираем по макс id)
#суммарное количество недобавленных мыслей
print(sorted([(value, key) for key, value in areas.items()], reverse=True)[:10])


print(total_think - sum(think_to_add.values()))


#print(think_to_add)

