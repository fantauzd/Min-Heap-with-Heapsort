# Name: Dominic Fantauzzo
# OSU Email: fantauzd@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 5 - MinHeap Implementation
# Due Date: 2/24/2024
# Description: Implementation of a MinHeap using a dynamic array.

from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)

    def swap(self, index1: int, index2: int) -> int:
        """
        Swaps the values at index 1 and index 2 in the heap and then returns index 2.
        Note that index 2 now holds the value that was at index 1. Operates in O(1) time complexity.
        """
        temp = self._heap[index2]
        self._heap[index2] = self._heap[index1]
        self._heap[index1] = temp
        return index2

    def add(self, node: object) -> None:
        """
        This method adds a new object to the MinHeap while maintaining heap property. In O(log N) time complexity.
        """
        # append the node to the end of the array
        self._heap.append(node)
        node_index = self._heap.length()-1
        # percolate up until min heap property is fulfilled or the node is the head, worst case in O(Log N)
        _percolate_up(self._heap, node_index)

    def is_empty(self) -> bool:
        """
        This method returns True if the heap is empty; otherwise, it returns False.
        """
        return self._heap.is_empty()

    def get_min(self) -> object:
        """
        This method returns an object with the minimum key, without removing it from the heap. If
        the heap is empty, the method raises a MinHeapException.
        """
        if self.is_empty():
            raise MinHeapException
        return self._heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        This method returns an object with the minimum key, and removes it from the heap. If the
        heap is empty, the method raises a MinHeapException.
        """
        if self._heap.is_empty():
            raise MinHeapException
        # save the object with min key for return
        result = self._heap.get_at_index(0)
        # overwrites the object with min key with the last object in the heap then percolates down
        if self._heap.length() > 1:
            self._heap.set_at_index(0, self._heap.pop())
        # if there is only one value left, we simply pop it
        else:
            self._heap.pop()
        _percolate_down(self._heap, 0, self.size())          # All operations are constant time except percolating down.
        return result

    def build_heap(self, da: DynamicArray) -> None:
        """
        This method receives a DynamicArray with objects in any order, and builds a proper
        MinHeap from them. The current content of the MinHeap is overwritten.
        """
        # clear the array and append values from the dynamic array parameter so heap is a copy of dynamic array
        # append is in amortized O(1) and we append n values where n is the number of values in the dynamic array,
        # thus, copying the array is in amortized O(n). We then build a heap on our array which is also in O(n). So,
        # the whole function is still in O(n).
        self.clear()
        for val in range(da.length()):
            self._heap.append(da.get_at_index(val))
        # find the first possible non-leaf (from the back of the array)
        i = (self.size()//2)-1
        # Move backwards one element at a time from the first non-leaf element.
        # Ensure every subtree rooted at that element’s original position will be a proper heap by percolating down.
        while i >= 0:
            _percolate_down(self._heap, i, self.size())
            i -= 1

    def size(self) -> int:
        """
        This method returns the number of items currently stored in the heap.
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        This method clears the contents of the heap.
        """
        if self.is_empty():
            return
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    Receives a DynamicArray and sorts its content in non-ascending order,
    using the Heapsort algorithm.
    """
    # find the first possible non-leaf (from the back of the array)
    i = (da.length() // 2) - 1
    # Move backwards one element at a time from the first non-leaf element.
    # Ensure every subtree rooted at that element’s original position will be a proper heap by percolating down.
    while i >= 0:
        _percolate_down(da, i, da.length())
        i -= 1
    # Now that the dynamic array is a heap, we can perform heapsort.
    k = da.length()-1
    # Beginning at the last element and moving backwards, swap the first element (min) with the kth element.
    # Then percolate down until reaching the kth element, so that the heap satisfies heap property and
    # any elements swapped from the first position are left in place.
    while k > 0:
        # swap first element with kth element
        temp = da.get_at_index(k)
        da.set_at_index(k, da.get_at_index(0))      # k is now in our sorted portion
        da.set_at_index(0, temp)
        _percolate_down(da, 0, k)                   # pass k so no percolating stops before sorted portion
        k -= 1


# It's highly recommended that you implement the following optional          #
# function for percolating elements down the MinHeap. You can call           #
# this from inside the MinHeap class. You may edit the function definition.  #
def _percolate_down(da: DynamicArray, i: int, k: int) -> None:
    """
    Swap the node with the smaller of its two children.
    Continue this process with the node until it becomes a leaf node or until the min heap property is restored.
    Runs in O(h) where h is the height of the node at index i. This is in O(Log N) where N is the number of nodes
    in the subtree beginning at the node at index i.

    :param i: The index of the node that we are percolating down

    :param k: The first index that is out of bounds for percolating down to.
    """
    # Continue percolating down while the node has a child (not a leaf)
    while (2*i+1) < k:
        # If the node only has a left child or the left child is smaller than right
        if (2*i+2) >= k or da.get_at_index(2*i+1) <= da.get_at_index(2*i+2):
            # If the node is not larger than its left child, it is finished percolating
            if da.get_at_index(i) <= da.get_at_index(2*i+1):
                return
            # swap the node with its left child and update index
            temp = da.get_at_index(i)
            da.set_at_index(i, da.get_at_index(2*i+1))
            da.set_at_index((2*i+1), temp)
            i = 2 * i + 1
        # If the right child is smaller than left
        elif da.get_at_index(2*i+2) < da.get_at_index(2*i+1):
            # If the node is not larger than its right child, it is finished percolating
            if da.get_at_index(i) <= da.get_at_index(2*i+2):
                return
            # swap the node with its right child and update index
            temp = da.get_at_index(i)
            da.set_at_index(i, da.get_at_index(2*i+2))
            da.set_at_index((2*i+2), temp)
            i = 2 * i + 2


def _percolate_up(da: DynamicArray, i: int) -> None:
    """
    Swap the node with its parent.
    Continue this process with the node until it becomes the root or until the min heap property is restored.
    Runs in O(Log N) where N is the number of nodes in the heap.

    :param i: The index of the node that we are percolating down
    """
    # While the node at 'i' has a parent (is not the root) and that parent is larger, we percolate upwards
    while (i-1)//2 >= 0 and da.get_at_index((i-1)//2) > da.get_at_index(i):
        # swap the node with its parent and update index
        temp = da.get_at_index(i)
        da.set_at_index(i, da.get_at_index((i-1)//2))
        da.set_at_index((i-1)//2, temp)
        i = (i-1)//2

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)
