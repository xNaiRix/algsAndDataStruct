def to4(n):
    if n == 0:
        return "0"
    ans = ""
    while n!= 0:
        ans = str(n%4) + ans
        n//=4
    return ans
def R(n):
    s = to4(n)
    if n%4 == 0:
        s = s + s[-2:]
    else:
        t = sum(int(x) for x in s)
        t*=4
        s += to4(t)
    return int(s, 4)

vars = []
for i in range(1, 5000000):
    r = R(i)
    if r > 211 and r%6 == 0:
        vars.append((r, i))
print(sorted(vars)[:10])
# print(R(3))