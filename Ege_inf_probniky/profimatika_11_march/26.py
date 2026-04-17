f = open("26.txt")
n,k = map(int, f.readline().split())
powers = []

models = []
i = 0
best_power = {}
for line in f:
    if i < n:
        powers.append(int(line))
        i += 1
    else:
        power, cost = map(int, line.split())
        models.append([power,cost])
        if cost not in best_power:
            best_power[cost] = power
        else:
            best_power[cost] = max(best_power[cost], power)

#print(best_power)
powers.sort()
models.sort()
#ставим третьим мин стоимость справа (включая данный)
models[-1].append(models[-1][1])
for i in range(len(models) - 2, -1, -1):
    models[i].append(min(models[i][1], models[i+1][2]))
# print(models[:20])
# print(powers[:20])
# print(best_power[120])
j = 0
chosen_models = []#[cost, power]

for i in range(n):
    while powers[i] > models[j][0]: j+=1
    #теперь мощностей достаточно
    #print(i, models[j])
    chosen_models.append([models[j][2], best_power[models[j][2]]])
print(sum(x[0] for x in chosen_models))
print(max([x[1] for x in chosen_models]))
