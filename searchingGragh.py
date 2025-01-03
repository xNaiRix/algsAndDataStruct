class binaryTree:
    def __init__(self, root = None):
        self.root = root
    def add(self, key):
        if self.root == None:
            self.root = Node(key)
            return -1
        cur = self.root
        while (key <= cur.key and cur.left != None) or (key > cur.key and cur.right != None):
            if key <= cur.key:
                cur = cur.left
            else:
                cur = cur.right
        ret = cur.key
        if key <= cur.key:
            cur.left = Node(key)
        else:
            cur.right = Node(key)
        return ret
class Node:
    def __init__(self, key, left = None, right = None):
        self.key = key
        self.left = left
        self.right = right
class Gragh:
    def __init__(self):
        self.g = []
        self.keys = {}
        self.n = 0
        self.Tree = binaryTree()
    def add(self, val):
        parent = self.Tree.add(val)
        self.g.append([])
        self.n += 1
        self.keys[val] = len(self.g)- 1
        for key, v in self.keys.items():
            if key < val or key == parent:
                self.g[v] += [len(self.g) - 1]
                self.g[len(self.g) - 1] += [v]
    def find_path_weigth(self, start, end):
        inf = 10**10
        dist = [inf] * self.n
        dist[self.keys[start]] = 0
        q = [self.keys[start]]#здесь именно индексы в keys
        while len(q) != 0:
            v = q[0]
            q = q[1:]
            for i in self.g[v]:
                if dist[i] == inf:
                    q += [i]
                    dist[i] = dist[v] + 1
        return dist[self.keys[end]]
import random
myG = Gragh()
verts = []
for i in range(2000):
    x = int(random.random() * 1000)
    myG.add(x)
    verts.append(x)
print(verts)
print(myG.find_path_weigth(verts[133], verts[1000]))
