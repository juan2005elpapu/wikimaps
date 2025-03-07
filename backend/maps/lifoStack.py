class LifoNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class LifoStack:
    def __init__(self):
        self.head = None
        self._size = 0

    def push(self, value):
        """Add an element to the top of the stack."""
        new_node = LifoNode(value)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def pop(self):
        """Remove and return the top element from the stack."""
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        popped_value = self.head.value
        self.head = self.head.next
        self._size -= 1
        return popped_value

    def peek(self):
        """Return the top element without removing it."""
        if self.is_empty():
            raise IndexError("Peek from an empty stack")
        return self.head.value

    def is_empty(self):
        """Check if the stack is empty."""
        return self._size == 0

    def size(self):
        """Return the number of elements in the stack."""
        return self._size

    def __iter__(self):
        """Iterate through the stack."""
        current = self.head
        while current:
            yield current.value
            current = current.next

    def get_all(self):
        """Return the entire stack as a list."""
        return list(self)

    def __repr__(self):
        return f"Stack({self.get_all()})"