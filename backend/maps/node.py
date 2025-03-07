class Node:
    def __init__(self, name, latitude, longitude):
        """Represents a node in a graph with a name and coordinates."""
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.neighbors = []  # List of (neighbor_node, weight)

    def add_neighbor(self, neighbor, weight=1):
        """Adds a neighboring node with an optional weight (default=1)."""
        self.neighbors.append((neighbor, weight))

    def __repr__(self):
        return f"Node({self.name}, {self.latitude}, {self.longitude})"
