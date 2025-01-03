class Node:
    def __init__(self, el = None, next = None):
        self.el = el
        self.next = next
    def __eq__(self, other):
        if not isinstance(other, Node):
            raise TypeError
        return self.el == other.el
class CustomList:
    def __init__(self):
        self.root = Node()
        self.len = 0
    def add(self, new_el, i):
        if i > self.len:
            raise IndexError
        self.len += 1
        if self.root.el == None:
            self.root = Node(new_el)
            return
        cur = self.root
        for cur_i in range(i - 1):
            cur = cur.next
        new_node = Node(new_el, cur.next)
        cur.next = new_node
    def append(self, new_el):
        self.add(new_el, self.len)
    def pop(self, i):
        if i >= self.len:
            raise IndexError
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
    def __getitem__(self, index):
        if isinstance(index, slice):
            new_list = CustomList()
            for i in range(index.start, index.stop, index.step):
                new_list.append(self.list[i])
            return new_list
        if not isinstance(index, int):
            raise TypeError
        if index < 0 or index >= self.len:
            raise IndexError
        cur = self.root
        for i in range(index):
            cur = cur.next
        return cur.el
    def __contains__(self, el):
        for i in range(self.len):
            if self.__getitem__(i) == el:
                return True
        return False
    def __add__(self, other):
        if not isinstance(other, CustomList):
            raise TypeError
        new_arr = self
        for i in range(other.len):
            new_arr.append(other[i])
        return new_arr


class CustomDict:
    def __init__(self, classes = CustomList(), list = CustomList()):
        self.classes = classes
        self.list = list
    def add(self, key, val, index):
        if not any(isinstance(key, x) for x in self.classes):
            raise TypeError
        mid = CustomList()
        mid.append(ElementInDict(key, val))
        self.list = self.list[:index] + mid + self.list[index + 1:]
    def add_class(self, new_class):
        self.classes.append(new_class)
    def delete(self, key):
        if not any(isinstance(key, x) for x in self.classes):
            raise TypeError
        for i in range(len(self.list)):
            if self.list[i] == ElementInDict(key):
                val = self.list[i].val
                self.list = self.list[:i] + self.list[i + 1:]
                return val
        raise KeyError
    def get(self, index):
        if not isinstance(index, int):
            raise TypeError
        if index < 0 or index >= len(self.list):
            raise IndexError 
        return (self.list[index].key, self.list[index].value)
class ElementInDict:
    def __init__(self, key, val = None):
        self.key = key
        self.val = val
    def __eq__(self, other):
        if not isinstance(other, ElementInDict):
            raise TypeError
        return self.key == other.key
print("true")