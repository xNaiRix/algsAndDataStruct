from itertools import permutations
s1 = set(frozenset(x) for x  in "234 157 178 16 267 45 235 3".split())
s2 = "N MQO NRP NRS OQS OT RQT PS"
alp = list(set("NMQONRPNRSOQSOTRQT"))
#print(alp)
for p in permutations(alp):
    s_copy = s2
    for letter, num in zip(p, "12345678"):
        s_copy = s_copy.replace(letter, num)
    if set(frozenset(x) for x in s_copy.split()) == s1:
        print(dict(zip("12345678", p)))
#{'1': 'O', '2': 'R', '3': 'N', '4': 'P', '5': 'S', '6': 'T', '7': 'Q', '8': 'M'} 
#R: 2
#2-1, 2-5, 2-7
#sum = 1+5+7 = 13