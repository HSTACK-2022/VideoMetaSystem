import heapq

def heap_sort(lst):
  h = []
  for val in lst:
    heapq.heappush(h, val)
  return [heapq.heappop(h) for _ in range(len(h))]

d = [6, 8, 3, 9, 10, 1, 2, 4, 7, 5]
new = heap_sort(d)
print(new)

resultVideoIDList = [311, 312, 315]

#def idlist(resultVideoIDList):

def rank():
#ranking algorithm
    for i in list(resultVideoIDList): # (resultVideoIDList)에 저장되어 있는 id로 메타데이터 가져옴
        print(i) #id
