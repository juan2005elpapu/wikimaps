class FifoNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class FifoQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def enqueue(self, value):
        """Add an element to the end of the queue."""
        new_node = FifoNode(value)
        if self.is_empty():
            self.head = new_node
        else:
            self.tail.next = new_node
        self.tail = new_node
        self._size += 1

    def dequeue(self):
        """Remove and return the first element from the queue."""
        if self.is_empty():
            raise IndexError("Dequeue from an empty queue")
        dequeued_value = self.head.value
        self.head = self.head.next
        if self.head is None:  # If the queue is now empty, update the tail
            self.tail = None
        self._size -= 1
        return dequeued_value

    def peek(self):
        """Return the first element without removing it."""
        if self.is_empty():
            raise IndexError("Peek from an empty queue")
        return self.head.value

    def is_empty(self):
        """Check if the queue is empty."""
        return self._size == 0

    def size(self):
        """Return the number of elements in the queue."""
        return self._size

    def __iter__(self):
        """Iterate through the queue."""
        current = self.head
        while current:
            yield current.value
            current = current.next

    def get_all(self):
        """Return the entire queue as a list."""
        return list(self)

    def __repr__(self):
        return f"Queue({self.get_all()})"