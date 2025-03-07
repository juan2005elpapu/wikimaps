import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from nodes.mapNode import MapNode
from dataStructures.fifoQueue import FifoQueue
from dataStructures.lifoStack import LifoStack

from math import radians, cos, sin, sqrt, atan2

class Graph:
    def __init__(self):
        # Almacena vértices en una cola FIFO (cada vértice es un MapNode)
        self.vertices = FifoQueue()
        # Almacena caminos en una pila LIFO; cada camino es una tupla (id1, id2, distancia)
        self.edges = LifoStack()

    def add_vertex(self, id, lat, lon):
        # Verifica si el vértice ya existe iterando sobre la cola FIFO
        for vertex in self.vertices:
            if vertex.value == id:
                return False
        self.vertices.enqueue(MapNode(id, lat, lon))
        return True

    def add_edge(self, id1, id2):
        v1 = self.get_vertex_by_id(id1)
        v2 = self.get_vertex_by_id(id2)
        if v1 is None or v2 is None:
            return False
        distance = self.calculate_distance(v1.lat, v1.lon, v2.lat, v2.lon)
        self.edges.push((id1, id2, distance))
        return True

    def delete_edge(self, id1, id2):
        # Reconstruye la pila LIFO excluyendo el camino a borrar.
        temp_stack = []
        deleted = False
        while not self.edges.is_empty():
            edge = self.edges.pop()
            if edge[0] == id1 and edge[1] == id2:
                deleted = True
                # No lo agrega a la pila temporal
            else:
                temp_stack.append(edge)
        # Vuelve a insertar los caminos que no fueron borrados
        for edge in reversed(temp_stack):
            self.edges.push(edge)
        return deleted

    def delete_vertex(self, id):
        # Reconstruir la FIFO sin el vértice a borrar.
        new_fifo = FifoQueue()
        deleted = False
        for vertex in self.vertices:
            if vertex.value == id:
                deleted = True
            else:
                new_fifo.enqueue(vertex)
        self.vertices = new_fifo

        # Borrar de la pila LIFO todos los caminos que involucren al vértice borrado
        temp_stack = []
        while not self.edges.is_empty():
            edge = self.edges.pop()
            if edge[0] == id or edge[1] == id:
                continue  # Se omite el camino que involucra al vértice borrado
            else:
                temp_stack.append(edge)
        for edge in reversed(temp_stack):
            self.edges.push(edge)
        return deleted

    def get_vertex_by_id(self, id):
        for vertex in self.vertices:
            if vertex.value == id:
                return vertex
        return None

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # Radio de la Tierra en km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c  # Distancia en km

    def get_all_vertices(self):
        # Devuelve el iterador de la cola FIFO
        return self.vertices

    def get_all_edges(self):
        # Devuelve el iterador de la pila LIFO
        return self.edges
