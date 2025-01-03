import random#в вершинах лежат целые числа (можно чтобы a < b <=> a <= b - 1)
def compare(x, y):
    return x[0] < y[0]
def isEqual(x, y):
    return x[0] == y[0]
class NodeInTreap:
    def __init__(self, el):
        self.el = el
        self.y = random.random()
        self.left = None
        self.right = None
    def getTree(self):
        if self.left == None and self.right == None:
            return [self.el]
        if self.left == None:
            return [self.el] + self.right.getTree()
        if self.right == None:
            return self.left.getTree() + [self.el]
        return self.left.getTree() + [self.el] + self.right.getTree()
class Treap:
    def __init__(self, compare = compare,isEqual = isEqual):
        self.root = None
        self.isEqual = isEqual#функция сравнения на ревенство
        self.compare = compare#функция сравнения элементов в ноде
    def merge(self, v, u):
        if v == None:
            return u
        if u == None:
            return v
        if v.y > u.y:
            v.right = self.merge(v.right, u)
            return v
        u.left = self.merge(v, u.left)
        return u
    def split(self, n_node, k_el):
        n = n_node
        if n == None:
            return (None, None)
        v,u = None, None
        if self.compare(k_el, n.el):
            v,n.left = self.split(n.left, k_el)
            u = n   
        else:
            n.right, u = self.split(n.right, k_el)
            v = n
        return (v, u)
    def find(self, key):
        t = self.split(self.root, key - 1)
        if t[1] == None:
            self.root = self.merge(t[0], t[1])
            return None
        left = t[0]
        t = self.split(t[1], key)
        mid, right = t[0], t[1]
        if mid == None:
            self.root = self.merge(self.merge(left, mid), right)
            return None
        self.root = self.merge(self.merge(left, mid), right)
        return mid.el
    def add(self, new_el):
        if self.find(new_el) != None:
            return 
        new_node = NodeInTreap(new_el)
        t = self.split(self.root, new_el)
        self.root = self.merge(self.merge(t[0], new_node), t[1])
    def remove(self, el):
        t = self.split(self.root, el)
        self.root = self.merge(t[0],t[1])
    def getTree(self):
        if self.root == None:
            return []
        return self.root.getTree()