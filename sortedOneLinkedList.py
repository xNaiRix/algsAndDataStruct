class CustomList:
    def __init__(self, cmp = lambda x, y: x < y):
        self.root = Node()
        self.len = 0
        self.cmp = cmp
    def add(self, new_el, i):
        if i > self.len:
            print("Index out of range")
            exit()
        self.len += 1
        if self.root.el == None:
            self.root = Node(new_el)
            return
        cur = self.root
        for cur_i in range(i - 1):
            cur = cur.next
        new_node = Node(new_el, cur.next)
        cur.next = new_node
    def sortedAdd(self, new_el):
        if self.root.el == None:
            self.root = Node(new_el, self.root)
            self.len += 1
            return
        if self.cmp(new_el, self.root.el):
            self.root = Node(new_el, self.root)
            self.len += 1
            return
        pred = self.root
        cur = pred.next
        self.len += 1
        while cur.el != None and self.cmp(cur.el, new_el):
            pred = pred.next
            cur = cur.next
        pred.next = Node(new_el, pred.next)
    def pop(self, i):
        if i >= self.len:
            print("index out of range")
            exit()
        tmpLen = self.len-1
        self.len -= 1
        cur = self.root
        if i == 0:
            self.root = self.root.next
            self.len = tmpLen
            return
        for j in range(i - 1):
            cur = cur.next
        cur.next = cur.next.next
    def printList(self):
        cur = self.root
        for i in range(self.len - 1):
            print(cur.el, end = ' -> ')
            cur = cur.next
        print(cur.el)
class Node:
    def __init__(self, el = None, next = None):
        self.el = el
        self.next = next
cur_el = input()
myList = CustomList()
while cur_el != '':
    myList.sortedAdd(int(cur_el))
    cur_el = input()
myList.printList()