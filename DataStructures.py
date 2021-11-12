# Module for managing data structures throughout the application

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

    # Helper function that returns the next object in the LL
    def returnLinkedListNext(self):
        return self.head.returnNext()