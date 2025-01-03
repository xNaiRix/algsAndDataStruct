class ElementInCustomList:
    def __init__(self, el = None, next = None):
        self.el = el
        self.next = next
    def __eq__(self, other):
        if not isinstance(other, ElementInCustomList):
            raise TypeError
        return self.el == other.el
class CustomList:
    def __init__(self):
        self.root = ElementInCustomList()
        self.len = 0
    def add(self, new_el, i):
        if i > self.len or i < 0:
            raise IndexError
        self.len += 1
        if i == 0:
            if self.root.el == None:
                self.root = ElementInCustomList(new_el)
                return
            self.root = ElementInCustomList(el=new_el, next=self.root)
            return
        if self.root.el == None:
            self.root = ElementInCustomList(new_el)
            return
        cur = self.root
        for cur_i in range(i - 1):
            cur = cur.next
        new_ElementInCustomList = ElementInCustomList(new_el, cur.next)
        cur.next = new_ElementInCustomList
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
    def printList(self):
        cur = self.root
        for i in range(self.len - 1):
            print(cur.el, end = ' -> ')
            cur = cur.next
        print(cur.el)
#myList1 = CustomList()
#myList1.append(1)
#myList1.append(4)
myList2 = CustomList()
for i in range(4):
    myList2.append(int(input()))
myList2.printList()

