from numpy.random import randint as r
import timeit
import matplotlib.pyplot as plt
quick = []
merge = []
x = []

#Down below implemented Quick and Merge Sort algorithms
def quick_sort(array):
    # base case
    if len(array) <= 1:
        return array
    # division and recursive step
    else:
        pivot = array.pop(0)
        left, right = [], []
        for element in array:
            if element < pivot:
                left.append(element)
            else:
                right.append(element)
        return quick_sort(left) + [pivot] + quick_sort(right)

def merge_sort(left, right):
    newList = []

    if len(left) == 1 and len(right) == 1:
        if (left[0] < right[0]):
            newList = left + right
        else:
            newList = right + left

    else:
        while len(left) >= 1 and len(right) >= 1:
            if left[0] <= right[0]:
                newList.append(left.pop(0))
            else:
                newList.append(right.pop(0))

        newList = newList + left
        newList = newList + right

    return newList

def mergeSort(list):
    if len(list) == 1:
        return list

        # split in 2
    left = list[0:len(list) // 2]
    right = list[len(list) // 2:]
    leftSorted = mergeSort(left)
    rightSorted = mergeSort(right)

    return merge_sort(leftSorted, rightSorted)

#Now generated a series of lists of 10**i random elements from 10 to 100000.
#They are then sorted using quicksort at first, then mergesort.
for i in range(6)[1:]:
    s=10**i
    x.append(s)
    a = r(10**i, size=s)
    a = list(a)
    quick.append(timeit.timeit('quick_sort(a)', number=10, globals=globals()))
    merge.append(timeit.timeit('mergeSort(a)', number=10, globals=globals()))

#Can be observed how much Quick Sort is faster than Merge Sort.
#This is because Merge Sort is a stable sorting algorithm, meaning that it keeps track of the original positions of the elements inside the array.
#These requires higher use of memory for Merge Sort.
#So, even if in the worst case scenario Quick Sort requires much more operations than Merge Sort, it rarely happens to have at random a reversely sorted list, ora an already sorted one, or a list of only one element repeated.
plt.plot(x, merge, 'g--', label='Merge Sort', )
plt.plot(x, quick, 'r:', label='Quick Sort', linewidth = 3)
plt.xscale('log') #used log scale to represent the growth of necessary time of execution to sort.
plt.xlabel('Array Size')
plt.ylabel('Execution Time (s)')
plt.title('Merge Sort vs Quick sort')
plt.xticks(x, [str(e)+ ' elements' for e in x])
plt.legend()
plt.show()