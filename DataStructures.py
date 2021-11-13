# Module for managing data structures throughout the application

import Package

# Class to manage a node object
class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

    # Return the data associated with a node
    def returnData(self):
        return self.data

    # Return the next item
    def returnNext(self):
        return self.next


# Class to manage the LinkedList class
class LinkedList:
    def __init__(self):
        self.head = Node()

    # Add a new object to an existing Linked List, at the end of the list
    def addToLinkedList(self, data):
        iterate = self.head
        if iterate.data is None:
            new_item = Node(data)
            self.head = new_item
        # list exists
        else:
            while iterate.next is not None:
                iterate = iterate.next
            new_item = Node(data)
            iterate.next = new_item
            new_item.next = None

    # Prints all items in a particular linked list to the screen
    def printAllLinkedList(self):
        iterate = self.head
        while iterate is not None:
            print(iterate.data)
            iterate = iterate.next

    # Helper function that returns linked list data
    def returnLinkedListData(self):
        return self.head.returnData()

    def returnHead(self):
        return self.head

    # Helper function that returns the next object in the LL
    def returnLinkedListNext(self):
        return self.head.returnNext()

    def setLinkedListData(self, data_to_set):
        self.head = data_to_set

    def setLinkedListNext(self, data_to_set_as_next):
        self.head.next = data_to_set_as_next


# Managing the Hash Table object. Initialization creates an emtpy hash table of 100 elements with index 0-99, if another
# number of hash table elements are not provided.
class HashTable:
    def __init__(self, size=100):
        self.size = size
        self.array = [LinkedList() for i in range(self.size)]

    def returnHashData(self):
        self.array[self].returnLinkedListData(self)

    # Calculate the index to use given the key value
    def calculateIndex(self, key):
        index = key % 100
        return index

    # Adds a new key / value pair to the hash table. Uses a linked list to avoid collisions where they might occur
    def addToHashTable(self, key, value):
        index = self.calculateIndex(key)
        if self.array[index].returnLinkedListData() is None:
            self.array[index].addToLinkedList(value)
        else:
            existing_list = self.array[index]
            existing_list.addToLinkedList(value)

    # Prints all hash table items if they exist
    def printAllHashTableContents(self):
        for i in range(len(self.array)):
            if self.array[i].returnLinkedListData() is not None:
                self.array[i].printAllLinkedList()


# is a list that includes the distances to all points from a given point
class AdjacencyList:
    def __init__(self, size):
        self.size = size
        self.list = [[] for i in range(self.size)]

    # Add a single distance to the adjacency list
    def addDistanceToAdacencyList(self, distance):
        self.list.insert(distance.location, distance.distance)

    def printAdjacencyList(self):
        for i in range(len(self.list)):
            print(self.list[i])

    def returnDistance(self, dest_index):
        return self.list[dest_index]


# class to manage the matrix that tracks distances between locations. Each position in the array represents a
# destination. For each destination there is an adjacency list which describes the distance to each location
# it is adjacent to
class DistanceMatrix:
    def __init__(self, size):
        self.size = size
        self.array = [AdjacencyList(self.size) for i in range(self.size)]

    # Adds an individual value to a matrix. In this case it also adds the converse since all distances are
    # bi-directional
    def addToMatrix(self, source_index, distance_obj):
        self.array[source_index].addDistanceToAdacencyList(distance_obj)
        # set the converse
        converse_distance = Package.Distance(source_index, distance_obj.distance)
        self.array[distance_obj.location].addDistanceToAdacencyList(converse_distance)

    # Returns the distance between two points. The inputs are both integers, that represent an address.
    def lookupDistance(self, source_index, dest_index):
        return self.array[source_index].returnDistance(dest_index)
