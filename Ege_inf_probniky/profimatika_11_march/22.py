#id, time, depends
ord = []
f = open("22.txt")
d = {}
used = {}
for line in f:
    ind, time, depends = line.split()
    d[ind] = [int(time), depends.split(";"), None]
    used[ind] = 0
used["0"] = 0
d["0"] = [0, [], 0]
def topsort(v):
    used[v] = 1
    for u in d[v][1]:
        if not used[u]:
            topsort(u)
    ord.append(v)
for v in  range(1, 26):#26
    if not used[str(v)]:
        topsort(str(v))


arr = []
for i in range(100):
    arr.append(list())#arr: [ [[],[]],
    #]
    arr[-1].append(list())#end
    arr[-1].append(list())#start

arr[0][0].append("0")
arr[0][1].append("0")
print(ord)
for ind in ord[1:]:
    t = d[ind][0]
    depends = d[ind][1]
    start_time = max(d[x][2] for x in depends)
    end_time = t + start_time
    print(ind)
    arr[start_time][1].append(ind)
    arr[end_time][0].append(ind)
    d[ind][2] = end_time

cnt = 0
for ends, starts in arr[:13]:#14
    cnt += len(set(starts)) - len(set(ends))
print({i: arr[i] for i in range(20)})#15
print(cnt)


