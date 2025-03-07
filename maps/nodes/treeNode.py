import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from nodes.node import Node

class TreeNode(Node):
    def __init__(self, valor, usuario=None):
 
        super().__init__(valor) 
        self.usuario = usuario  
        self.hijo = None  
        self.hermano = None  

    def agregar_hijo(self, nuevo_hijo):
        if not self.hijo:
            self.hijo = nuevo_hijo  
        else:
            actual = self.hijo
            while actual.hermano:
                actual = actual.hermano  
            actual.hermano = nuevo_hijo 

    def buscar_nodo(self, valor_buscar):
        if self.valor == valor_buscar:
            return self  
        if self.hijo:
            encontrado = self.hijo.buscar_nodo(valor_buscar)
            if encontrado:
                return encontrado
        if self.hermano:
            return self.hermano.buscar_nodo(valor_buscar)
        else:
            return None  