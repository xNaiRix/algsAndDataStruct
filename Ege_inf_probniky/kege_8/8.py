from itertools import product
alp = "01234"
ans = []
for p in product(alp, repeat = 6):
    if p[0] != "0" and p.count("3") == 2 and p.count("1")>=2:
        ans.append(''.join(p))
print(ans)
print(len(ans))