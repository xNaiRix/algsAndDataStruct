exp = input()
ops = ["and", "or", "not", "<=", "==", "!=", "in"]
exp_c = exp
for op in ops:
    exp = exp.replace(op, " " + op + " ")
    exp_c = exp_c.replace(op, " ")
while "  " in exp_c or "  " in exp:
    exp_c = exp_c.replace("  ", " ")
    exp = exp.replace("  ", " ")
vars = sorted(set(x for x in exp_c.split() if x != " "), key = lambda x: x.islower())
print(vars)
def f(x, vals, vars, exp):#vals: [[13,20], [421,2100]], vars: ["[]","[]", x]
    for val, var in zip(vals, vars[:-1]):
        exp = exp.replace(var, str(val))
    exp = exp.replace(vars[-1], str(x))
    print(exp)
    return eval(exp)
print(f(14, [[10,14,20], [15, 20], [10, 25]],vars,exp))

#Пока только наброски ВООБЩЕ НЕ ДОДЕЛАНО