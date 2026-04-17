from functools import cache
@cache
def q(n):
    if n >= 210000: return n + 4
    return q(n + 3) + 2

@cache
def g(n):
    if n >= 11: return g(n-3) + 5
    return q(n) + 6

@cache
def f(n):
    if n>=4300: return g(n-3)
    return f(n+2) + 2

for i in range(220000, 0, -1): q(i)
for i in range(220000): g(i)
for i in range(220000,0,-1): f(i)
print(f(1))#361458