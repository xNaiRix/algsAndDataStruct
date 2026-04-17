def f(s, m):
    if s >= 167: return m%2 == 0
    if m == 0: return 0
    h = [f(s + 1, m - 1), f(s + 2, m - 1), f(s * 3, m - 1)]
    return all(h) if (m+1)%2 == 1 else any(h)
print([s for s in range(1, 167) if not f(s, 1) and f(s, 2)])#all, any, 55
print([s for s in range(1, 167) if not f(s, 1) and f(s, 3)])#all, any, 53,54
print([s for s in range(1, 167) if not f(s, 2) and f(s, 4)])#all, any, 52

 