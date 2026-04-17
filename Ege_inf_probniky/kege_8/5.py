def f(n):
    s = f"{n:b}"
    if n%2 == 0:
        s += s[-3:]
    else:
        s = "1" + s +"01"
    return int(s, 2)

for i in range(1, 10000000):
    r = f(i)
    if abs(r - 155) <= 9:
        print(i, r)
#18 146
#20 164
#MINdelta = 9