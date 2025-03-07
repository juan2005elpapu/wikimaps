import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from nodes.node import Node

class MapNode(Node):
    def __init__(self, id, lat, lon):
        super().__init__(id)
        self.lat = lat
        self.lon = lon
