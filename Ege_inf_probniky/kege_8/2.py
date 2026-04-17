from itertools import permutations, product
def f(x,y,z,w):
    return (not (x and z and not y) )\
        and (not (w and x)) and \
        (not (( not (y or x)) == w ))

for x1,x2,x3,x4,x5 in product([0,1], repeat = 5):
    t = (
        (0,1,x1,x2),
        (0,x3,1,x4),
        (x5,1,1,1)
    )
    if len(t) != len(set(t)): continue
    for p in permutations("xyzw"):
        if [f(**dict(zip(p, line))) for line in t] == [1,1,1]:
            print(''.join(p))
#xzwy