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

h=BinHeap()

x=range(10**5)
a=random.sample(x,10**5)
insertionsTimes=[]
getMaxTimes=[]
deleteMaxTimes=[]

for e in a:
    # measured times of insertions and the time necessary to get the max while the heap increases in size
    insertionsTimes.append(timeit.timeit('h.insert(e)', number=1, globals=globals()))
    getMaxTimes.append(timeit.timeit('h.heapList[1]', number=1, globals=globals()))

for _ in x:
    #Now the heap gets gradually deleted by deleting the max, so that it'll be possible to whatch the time it takes depending on the size of the heap
    deleteMaxTimes.append(timeit.timeit('h.delMax()', number=1, globals=globals()))

plt.figure(1)
#Can be observed, in the zommed in subplot, how evident is the logarithmic growth of the necessary time to insert an element.
plt.subplot(211)
plt.title('Insertion of single elements in a Max Heap increasing in size')
plt.ylabel('Time of insertion (s)')
plt.scatter(x,insertionsTimes)
plt.ylim((0, max(insertionsTimes)+ 0.00005))
plt.subplot(212)
plt.ylabel('Time of insertion (s)')
plt.xlabel('Max Heap size')
plt.scatter(x,insertionsTimes)
plt.ylim((0, 0.000010))

plt.figure(2)
#Can be observed how it's constant the time to obtain the Max in a MaxHeap.
#This is because it is always at the root of the tree, or, also, at the first position of the array like structure of the heap.
#Can be observed also for some cases how to get the max is actually istantaneous!
plt.subplot(211)
plt.title('Get the Max in a Max Heap increasing in size')
plt.ylabel('Time necessary to get the Max (s)')
plt.scatter(x,getMaxTimes,s=0.8)
plt.ylim((-0.000005,max(getMaxTimes)+0.000005))
plt.subplot(212)
plt.ylabel('Time necessary to get the Max (s)')
plt.xlabel('Max Heap size')
plt.scatter(x,getMaxTimes, s=0.8)
plt.ylim(-0.00000015, 0.0000020)

plt.figure(3)
#Can be obsrved how, also here, the growth of time necessary to delete the max is logarithmic with respect to the size of the heap.
#This similarity with the insertion is not casual, since the number of percolations necessary to find the new Max is similar to the one of percolations performed with the insertion.
plt.subplot(211)
plt.title('Deletion of the Max in a Max Heap increasing in size')
plt.ylabel('Time necessary to delete the Max (s)')
plt.scatter(x[::-1], deleteMaxTimes)
plt.ylim(0, max(deleteMaxTimes))
plt.subplot(212)
plt.ylabel('Time necessary to delete the Max (s)')
plt.xlabel('Max Heap size')
plt.scatter(x[::-1],deleteMaxTimes)
plt.ylim(-0.00001, 0.00003)
plt.show()