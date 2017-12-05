# Many modifications to BST class have been done both to make the BST functional to be timed and to repair its implementation, wrong in the deletion mechanisms
# Down below the modifications are listed under the interested functions, but it's necessary to define some concepts that are used in the new implementation.
# Depth: the distance in terms of nodes from the root of the tree. Functional to time the Get method.
# Node run: distance in terms of nodes from a given node. Functional to time the findMax method.
# Modified functions are: get mechanism, deletion mechanism
# Newly implemented functions are: getNode, findMax

import random
import timeit
import matplotlib.pyplot as plt


class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def put(self, key, val):

        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
        else:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)

    def __setitem__(self, k, v):
        self.put(k, v)

    def get(self, key):
        if self.root:
            res, lev = self._get(key, self.root, 0)  # only modification is the depth parameter 0 (from root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def getNode(self, key):
        # Implemented this function so to return both the Node of a key and its depth in the tree, on the base of get
        if self.root:
            res, lev = self._get(key, self.root, 0)
            if res:
                return res, lev
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode, depth):
        # Modified _get implementation so to keep track of the depths of the nodes too
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode, depth
        elif key < currentNode.key:
            depth += 1
            return self._get(key, currentNode.leftChild, depth)
        else:
            depth += 1
            return self._get(key, currentNode.rightChild, depth)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self._get(key, self.root, 0):
            return True
        else:
            return False

    # Deletion mechanism has been repaired. Main mistake was that in the original implementation lot of confusion has rised between keys and nodes
    # Main mechanism of repair is been to add a parameter containing the nodes in the function spliceOut, findSuccessor and findMin
    def delete(self, key):
        if self.size > 1:
            nodeToRemove, l = self._get(key, self.root, 0)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size - 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')

    def __delitem__(self, key):
        self.delete(key)

    def spliceOut(self, succ):
        if succ.isLeaf():
            if succ.isLeftChild():
                succ.parent.leftChild = None
            else:
                succ.parent.rightChild = None
        elif succ.hasAnyChildren():
            if succ.hasLeftChild():
                if succ.isLeftChild():
                    succ.parent.leftChild = succ.leftChild
                else:
                    succ.parent.rightChild = succ.leftChild
                succ.leftChild.parent = succ.parent
            else:
                if succ.isLeftChild():
                    succ.parent.leftChild = succ.rightChild
                else:
                    succ.parent.rightChild = succ.rightChild
                succ.rightChild.parent = succ.parent

    def findSuccessor(self, currentNode):
        succ = None
        if currentNode.hasRightChild():
            succ = self.findMin(currentNode.rightChild)
        else:
            if currentNode.parent:
                if currentNode.isLeftChild():
                    succ = currentNode.parent
                else:
                    currentNode.parent.rightChild = None
                    succ = currentNode.parent.findSuccessor(currentNode)
                    currentNode.parent.rightChild = currentNode
        return succ

    def findMin(self, cN=None):
        # Here below, in particular, modified findMin so to be called both alone to get the general Min and to make it functional starting from a given node.
        if cN:
            current = cN
        else:
            current = self.root
        while current.hasLeftChild():
            current = current.leftChild
        return current

    def findMax(self, cN=None):
        # Implemented as requested, on the bases of findMin. Morover, kept track of Nodes run to find the Max.
        run = 0
        if cN:
            current = cN
        else:
            current = self.root
        while current.hasRightChild():
            current = current.rightChild
            run += 1
        return current, run

    def remove(self, currentNode):
        if currentNode.isLeaf():  # leaf
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren():  # interior
            succ = self.findSuccessor(currentNode)
            self.spliceOut(succ)
            currentNode.key = succ.key
            currentNode.payload = succ.payload

        else:  # this node has one child
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                elif currentNode.isRightChild():
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.key,
                                                currentNode.leftChild.payload,
                                                currentNode.leftChild.leftChild,
                                                currentNode.leftChild.rightChild)
            else:
                if currentNode.isLeftChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.key,
                                                currentNode.rightChild.payload,
                                                currentNode.rightChild.leftChild,
                                                currentNode.rightChild.rightChild)



tree = BinarySearchTree()

x = range(10 ** 6)
a = random.sample(x, 10 ** 6)
times = []
for e in a:
    times.append(timeit.timeit('tree[e]=e', number=1, globals=globals()))
    #kept track of times while building the BST

plt.figure(0)
#Can be observed a logarithmic growth, as expected, in the second subplot.
plt.subplot(211)
plt.title('Insertion of single elements in a BST increasing in size')
plt.ylabel('Time of insertion (s)')
plt.scatter(x, times)
plt.ylim((-0.0001, max(times)))
plt.subplot(212)
#Zoomed in where logarithmic growth is evident
plt.ylabel('Time of insertion (s)')
plt.xlabel('BST size')
plt.scatter(x, times)
plt.ylim((0, 0.000015))



#for the following timings initialized a simpler tree to make computation faster
t = BinarySearchTree()
z = random.sample(range(10 ** 3), 10 ** 3)
for e in z:
    t[e] = e

Leaf = []
SingleBranch = []
DoubleBranch = []
getTimes = dict()
findMaxTimes = dict()

for e in z:
    n, l = t.getNode(e)

    if l not in getTimes:
        getTimes[l] = []
    getTimes[l].append(timeit.timeit('t[e]', number=10, globals=globals()))

    r = t.findMax(n)[1]
    #Here are found the nodes run, so to make them keys of a dictionary collecting lists with all the times related to that distance
    if r not in findMaxTimes:
        findMaxTimes[r] = []
    findMaxTimes[r].append(timeit.timeit('t.findMax(n)', number=10, globals=globals()))

    T = t
    #Everytime the loop is entered, a momentary tree equal to t is created.
    #This is to be sure that the deletions are done without altering definitively the structure of the tree.
    #Then the node is categorized as Leaf, Single Branching or Double Branching; than deleted. Measured the time of deletion and collected inside its proper list.
    if n.isLeaf():
        Leaf.append(timeit.timeit('T.delete(e)', number=1, globals=globals()))
    elif n.hasBothChildren():
        DoubleBranch.append(timeit.timeit('T.delete(e)', number=1, globals=globals()))
    elif (n.hasRightChild() and not n.hasLeftChild()) or (n.hasLeftChild() and not n.hasRightChild()):
        SingleBranch.append(timeit.timeit('T.delete(e)', number=1, globals=globals()))

plt.figure(1)
#There is a direct proportionality between the time get() takes to find the key and the number of nodes of distance from the root (get() always starts from root)
#So it's been decided to represent the relation between the time get() takes to find the node and its distance from root.
#Can be observed linear relationship between these elements.
plt.title('Get of all the elements in a given BST')
plt.xlabel('Depth of the element in the BST')
plt.ylabel('Time necessary to get the element (s)')
plt.xticks(range(len(getTimes)))
m = 0
for k, v in getTimes.items():
    for e in v:
        plt.scatter(k, e)
        if e > m:
            m = e
plt.ylim(0, m + 0.00001)

plt.figure(2)
#There is direct proportionality between the time findMax() takes to find the Max and the number of nodes of distance from the starting one (which can be given as argument)
#Represented here the relationship between the time findMax() takes to find the max from each node of the tree and its distance from it (in terms of nodes).
#Can be observed linear relationship between these elements.
plt.title('Find the Max from every node of the BST')
plt.xlabel('Number of nodes run to find the Max')
plt.ylabel('Time necessary to find the Max (s)')
plt.xticks(range(len(findMaxTimes)))
m = 0
for k, v in findMaxTimes.items():
    for e in v:
        plt.scatter(k, e)
        if e > m:
            m = e
plt.ylim(0, m + 0.00001)

plt.figure(3)
#Here, denoted is the relationship between the branching of the node we delete and the time it takes to finish the execution .
#Should be noticed that:
#A Leaf will require less time, since there is not any rearrangement of the tree, just needed the time to find its node (uses get()).
#A Single Branching node will require a little rearrangement of the tree, since will be enough just to replace it with its child node.
#A Double Branching node, instead, will require an operation to find its successor, then a structural rearrangement of the tree, so it's expected to take the most of the time.
#Can be observed, so, three different clusters that will group the time of deletion of all the nodes of the tree, after that they have been categorized thanks to getNode().
for e in Leaf:
    plt.scatter(0, e)
for e in SingleBranch:
    plt.scatter(1, e)
for e in DoubleBranch:
    plt.scatter(2, e)
plt.ylim((0, max(DoubleBranch)))
plt.title('Deletion of all the elements of a given BST')
plt.xlabel('Kind of Branching')
plt.ylabel('Time necessary to Delete the element (s)')
plt.xticks(range(3), ['Leafs', 'Single Branching', 'Double Branching'])
plt.show()