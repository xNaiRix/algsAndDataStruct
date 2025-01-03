ord = list(map(int,input().split(',')))
def add(el, tree):
    if tree == None:
        return [el, None, None]
    if el <= tree[0]:
        tree[1] = add(el, tree[1])
        return tree
    elif el > tree[0]:
        tree[2] = add(el, tree[2])
        return tree
    return tree
tree = None
for i in ord:
    tree = add(i, tree)
#деерво построено, теперь выводим

def mySort(tree):
    if tree[1] == None and tree[2] == None:
        return [tree[0]]
    right = []
    left = []
    if tree[2] != None:
        right = mySort(tree[2])
        if type(right) != list:
            right = [right]
    if tree[1] != None:
        left = mySort(tree[1])
        if type(left) != list:
            left = [left]
    return right + [tree[0]] + left
print(mySort(tree))  
    
