def f(s1, s2, m):
    if s1 + s2 >= 81:
        return m%2 == 0
    if m == 0: return 0
    h = [f(s1+1, s2, m - 1), f(s1*2, s2, m - 1),
         f(s1, s2+1, m- 1), f(s1, s2*2, m - 1)]
    return any(h) if m%2 == 1 else all(h)

print([s for s in range(1, 74) if f(7, s, 2)])#s_min = 19 (any any)
print([s for s in range(1, 74) if not f(7, s, 1) and f(7, s, 3)])#33 36
print([s for s in range(1, 74) if not f(7, s, 2) and f(7, s, 4)])#32+35=67