from itertools import product, permutations
def f(x,y,z,w):
    return (((x and y) <= (not z)) and (x<= y)) or w

for x11,x13,x14,x22,x23,x31 in product([0,1], repeat = 6):
    t = (
        (x11, 0, x13, x14),
        (1, x22, x23, 1),
        (x31, 1, 0 , 0)
    )
    if len(set(t)) != len(t): continue
    for p in permutations("xyzw"):
        if [f(**dict(zip(p, line))) for line in t] == [0,0,0]:
            print(''.join(p))