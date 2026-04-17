def f(start, end):
    if start <= end:
        return start == end
    return f(start - 2, end) + f(start - 6, end) + f(start//2, end)
#111->22 без 35
with35 = f(111,35) * f(35, 22)
every = f(111,22)
print(every - with35)#423926