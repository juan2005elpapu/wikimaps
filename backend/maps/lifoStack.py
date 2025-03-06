class LIFOStack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)  

    def pop(self):
        if self.is_empty():
            return None
        return self.stack.pop()  

    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]  

    def is_empty(self):
        return len(self.stack) == 0

    def size(self):
        return len(self.stack)

    def __repr__(self):
        return f"LIFOStack({self.stack})"
