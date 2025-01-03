leos = []
def getLeos(n):
    leos.append(1)
    leos.append(1)
    i = 1
    while leos[i] <= n:
        leos.append(leos[i - 1] + leos[i] + 1)
        i += 1
def sift(heap):
    if type(heap) != list:
        return
    if type(heap[1]) == list:
        if heap[1][0] > heap[0]:
            heap[1][0], heap[0] = heap[0], heap[1][0]
    elif heap[1] > heap[0]:
        heap[1], heap[0] = heap[0], heap[1]
    if type(heap[2]) == list:
        if heap[2][0] > heap[0]:
            heap[2][0], heap[0] = heap[0], heap[2][0]
    elif heap[2] > heap[0]:
        heap[2], heap[0] = heap[0], heap[2]
    sift(heap[1])
    sift(heap[2])
def buildTree(arr):
    getLeos(len(arr))
    heaps = []
    n = len(arr)
    for el in arr:
        fl = False
        #идём по уже созданным кучам, надо найти 2, которые можно объединить
        for i in range(len(heaps) - 1):
            heap  = heaps[i]
            nextHeap = heaps[i + 1]
            heapLen = heap[3] if (type(heap) == list) else 1#если heap - число, то это лист, то есть размер 1
            #иначе размер всегда хранится в 3 индексе
            nextHeapLen = nextHeap[3] if (type(nextHeap) == list) else 1
            if (heapLen + nextHeapLen + 1) in leos:
                heaps.remove(heap)
                heaps.remove(nextHeap)
                newHeap = [el, heap, nextHeap, heapLen+nextHeap+1]
                sift(newHeap)
                heaps.insert(i, newHeap)#туда, откуда забрали 2 кучи, туда ставим
                fl = True
        if not fl:
            heaps.append(el)#если элементом не получилось объединить 2 кучи,то создаем ещё одну кучу
    return heaps
arr = [3, 1, 2, 4, 22, 4, 2]
print(buildTree(arr))
