from itertools import permutations
alp = "ПРОФИМАТИКА"
words = []
for p in permutations(alp):
    w = ''.join(p)
    if w[0] != "П" and "ИИ" not in w:
        words.append(w)
words = list(set(words))
print(len(words))#7439040
#print(words)