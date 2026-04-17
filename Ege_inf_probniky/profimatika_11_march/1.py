from itertools import permutations
s = set(frozenset(x) for x in "3456 3567 126 17 127 123 245".split())
s2 = "БД АВГ БГД БВЕК ГКД ГЕД ВЕКА"
for p in permutations("АБВГДЕК"):
    s_copy = s2
    for letter, num in zip(p, "1234567"):
        s_copy = s_copy.replace(letter, num)
    # print()
    # print(s_copy)
    s_copy = set(frozenset(x) for x in s_copy.split()) 
    # print(p, s_copy)
    if s_copy == s:
        print(''.join(p))
        break