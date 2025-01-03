class Node:
    def __init__(self, key):
        self.key = key
class binaryTree:#удаление написать с нуля. Добавление работает, наверное, сделать через рекурсию
    def __init__(self, root = None, left = None, right = None):
        self.root = root
        self.left = left
        self.right = right
    def add(self, key):
        if self.root == None:
            self.root = Node(key)
            return
        if key <= self.root.key:
            if self.left == None:
                self.left = binaryTree(Node(key))
                return
            self.left.add(key)
            return
        if self.right == None:
            self.right = binaryTree(Node(key))
            return
        self.right.add(key)
    
    def pop(self, key):
        if self.root == None:
            return
        if key == self.root.key:
            if self.left == None and self.right == None:
                self.root = None
                return
            if self.left == None:
                self.left = self.right.left
                self.root.key = self.right.key
                self.right = self.right.right
                return
            if self.right == None:
                self.right = self.left.right
                self.root = self.left.root
                self.left = self.left.left
                return
            #идём вниз до левого листа (самое левое в правом поддереве)
            cur = self.right
            if cur.left == None:
                cur.left = self.left
                self = cur
                return
            while cur.left.left != None:
                cur = cur.left
            self.root = cur.left.root#значение отправляем наверх
            cur.left = cur.left.right#у нашего "левого листа" может быть ещё правое поддерево
            return
        if key < self.root.key:
            self.left.pop(key)
            return
        self.right.pop(key)
myTree = binaryTree()
myTree.add(3)
myTree.add(1)
myTree.add(4)
myTree.pop(1)
print("end")