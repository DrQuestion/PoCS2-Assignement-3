#The original implementation was a Min Heap, so it's been modified to a Max Heap, as requested
import random
import timeit
import matplotlib.pyplot as plt

class BinHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0


    def percUp(self,i):
        while i // 2 > 0:
          if self.heapList[i] > self.heapList[i // 2]:
             tmp = self.heapList[i // 2]
             self.heapList[i // 2] = self.heapList[i]
             self.heapList[i] = tmp
          i = i // 2

    def insert(self,k):
      self.heapList.append(k)
      self.currentSize = self.currentSize + 1
      self.percUp(self.currentSize)

    def percDown(self,i):
      while (i * 2) <= self.currentSize:
          mc = self.maxChild(i)
          if self.heapList[i] < self.heapList[mc]:
              tmp = self.heapList[i]
              self.heapList[i] = self.heapList[mc]
              self.heapList[mc] = tmp
          i = mc

    def maxChild(self,i):
      if i * 2 + 1 > self.currentSize:
          return i * 2
      else:
          if self.heapList[i*2] > self.heapList[i*2+1]:
              return i * 2
          else:
              return i * 2 + 1

    def delMax(self):
      retval = self.heapList[1]
      self.heapList[1] = self.heapList[self.currentSize]
      self.currentSize = self.currentSize - 1
      self.heapList.pop()
      self.percDown(1)
      return retval

    def buildHeap(self,alist):
      i = len(alist) // 2
      self.currentSize = len(alist)
      self.heapList = [0] + alist[:]
      while (i > 0):
          self.percDown(i)
          i = i - 1


x=range(10**5)
indexes=range(0,10**5,100)
insertionsTimes=[]
getMaxTimes=[]
deleteMaxTimes=[]

#Here follow 5 cycles, in which each time a Heap is initialized and gradually built, got the max and deleted the max.
for i in range(5):
    h=BinHeap()
    a=random.sample(x,10**5)
    for e in a:
        # measured times of insertions and the time necessary to get the max while the heap increases in size
        insertionsTimes.append(timeit.timeit('h.insert(e)', number=1, globals=globals()))
        getMaxTimes.append(timeit.timeit('h.heapList[1]', number=1, globals=globals()))
    for _ in x:
        # Now the heap gets gradually deleted by deleting the max, so that it'll be possible to whatch the time it takes depending on the size of the heap
        deleteMaxTimes.append(timeit.timeit('h.delMax()', number=1, globals=globals()))

#initialized three dictionaries: their keys will be the selected indexes of reference
#their values will be lists containing all the times that have been necessary to insert/delete the max/get the max for that specific ith element among the 5 Max Heaps
d=dict()
D=dict()
gm=dict()

for i in indexes:
    d[i]=[]
    D[i]=[]
    gm[i]=[]
    for e in range(5):
        d[i].append(insertionsTimes[e*(10**5)+i])
        D[i].append(deleteMaxTimes[e*(10**5)+i])
        gm[i].append(getMaxTimes[e*(10**5)+i])

#initialized some variables that will be used to keep track ov the maximum values in the next phase.
m=0
M=0
n=0

#Here below from all the lists in the dictionaries only the median is conserved
#Chosed the median since it is a good statistical unit rarely affected by outliers (so to finally reduce noise)
for i in indexes:
    d[i]=sorted(d[i])
    d[i] = d[i][2]
    if d[i]>m: m=d[i]
    D[i]=sorted(D[i])
    D[i]=D[i][2]
    if D[i]>M: M=D[i]
    gm[i]=sorted(gm[i])
    gm[i] = gm[i][2]
    if gm[i] > n: n = gm[i]

plt.figure(1)
#Can be observed how evident is the logarithmic growth of the necessary time to insert an element.
plt.title('Insertion of single elements in a Max Heap increasing in size, each 100 elements')
plt.ylabel('Time of insertion (s)')
plt.xlabel('Max Heap size')
plt.scatter(d.keys(),d.values(),s=4,c='y')
plt.ylim((0, m+0.000004))

plt.figure(2)
#Can be observed how it's constant the time to obtain the Max in a MaxHeap.
#This is because it is always at the root of the tree, or, also, at the first position of the array-like structure of the heap.
plt.title('Get the Max in a Max Heap increasing in size')
plt.ylabel('Time necessary to get the Max (s)')
plt.xlabel('Max Heap size')
plt.scatter(gm.keys(),gm.values(), s=3,c='c')
plt.ylim(0, n)

x=list(D.keys())
y=D.values()
plt.figure(3)
#Can be obsrved how, also here, the growth of time necessary to delete the max is logarithmic with respect to the size of the heap.
#This similarity with the insertion is not casual, since the number of percolations necessary to find the new Max is similar to the one of percolations performed with the insertion.
plt.title('Deletion of the Max in a Max Heap increasing in size, each 100 elements')
plt.ylabel('Time necessary to delete the Max (s)')
plt.xlabel('Max Heap size')
plt.scatter(x[::-1],y,s=4,c='g')
plt.ylim(0, M)
plt.show()