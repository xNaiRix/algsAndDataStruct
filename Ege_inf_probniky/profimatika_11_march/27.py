file = "Ege_inf_probniky\\profimatika_11_march\\27B.txt"
a = [list(map(float, line.split())) for line in open(file)]
eps = 1
r = []
from math import dist
for p in a:
    t = [[p]]
    for cl in r:
        if any(dist(p, q) < eps for q in cl):
            t[0] += cl
        else:
            t += [cl]
    r = t
print([len(x) for x in r])
r.sort(key = lambda x: len(x))
mids = []
for cl in r:
    cur_mid = None
    cur_sum = 1000000000000000000000
    for p in cl:
        sm = sum(dist(p,q) for q in cl)
        if sm <= cur_sum:
            cur_sum = sm
            cur_mid = p
    mids.append(cur_mid)

def getP1():
    return min(dist((5., 6.), mid) for mid in mids)
def getP2():
    return max(dist((5., 6.), mid) for mid in mids)

def getQ1():
    return sum(dist(mids[-1], q) <=1.5 for q in r[-1])
def getQ2():
    return sum(dist(mids[-1], q) <=0.95 for q in r[-1])

def my_ceil(P):
    return int(P*10000)
print('P1=',my_ceil(getP1()), " P2=", my_ceil(getP2()))#11593 66776
print('Q1=',getQ1(), " Q2=", getQ2())#398 278
