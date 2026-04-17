part = "A"
f = open(f"27{part}.txt")
a = [list(map(float, line.split())) for line in f]
r = []
eps = 1.5
from math import dist
for p in a:
    t = [[p]]
    for cl in r:
        if any(dist(p,q) < eps for q in cl):
            t[0] += cl
        else: t += [cl]
    r = t
r.sort(key = lambda x : len(x), reverse=True)
print(len(r))
print([len(cl) for cl in r])
mids = []
for cl in r:
    mid = min([[sum(dist(p, q) for q in cl), p] \
               for p in cl])[1]
    mids.append(mid)
print(mids)
def Sx():
    cl = r[-1]
    mid = mids[-1]
    sm = sum(p[0] for p in cl if dist(mid, p) < 1.)
    sm -= mid[0]#центр кластера не берется
    return sm

def Sy():
    cl = r[0]
    mid = mids[0]
    sm = sum(p[1] for p in cl if dist(mid, p) < 1.)
    sm -= mid[1]#центр кластера не берется
    return sm
    
def Q1():
    if part != "B": return 0
    anomalies = []
    for _ in r[3:]:
        anomalies += _
    cl_mids = mids[:3]
    mx = max(dist(p, q) for p in anomalies for q in cl_mids)
    return mx
def Q2():
    if part != "B": return 0
    anomalies = []
    for _ in r[3:]:
        anomalies += _
    cl_mids = mids[:3]
    mn = min(dist(p, q) for p in anomalies for q in cl_mids)
    return mn

def form(n): return int(abs(n) * 10000)
print("TASK A:", form(Sx()), form(Sy()))#46645713 3972919
print("TASK B:", form(Q1()), form(Q2()))