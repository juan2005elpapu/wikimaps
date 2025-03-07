from node import Node

class MapPointer:
    def __init__(self, node, color="blue", size=10):
        self.node = node  # The node associated with the pointer
        self.color = color
        self.size = size

    def get_location(self):
        """Returns the latitude and longitude of the pointer's node."""
        return (self.node.latitude, self.node.longitude)

    def __repr__(self):
        return f"Pointer(Node={self.node.name}, Location={self.get_location()})"

