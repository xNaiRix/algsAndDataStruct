from functools import cache
@cache
def g(n):
    if n >= 250000:
        return n//20 + 45
    return g(n + 9) - 2
@cache
def f(n):
    if n >= 25:
        return f(n - 6) + 4137
    return 7 * (g(n - 9) - 40)

for i in range(250009, -1, -1): g(i)
for i in range(100, -1, -1): f(i)
print(f(680))#153727