import os
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dataStructures.fifoQueue import FifoQueue
from nodes.treeNode import TreeNode

cola_comentarios = FifoQueue()
nodo_seleccionado = None

def mostrar_arbol(lugar):
    lugar.mostrar()

def agregar_comentario(lugar, comentario):
    from flask import session
    usuario = session.get("username", "Anónimo")
    
    # Buscar si existe ya un árbol para este lugar
    nodo_existente = None
    current = cola_comentarios.head
    
    while current:
        if hasattr(current, 'value'):
            tree_node = current.value
            if tree_node.value == lugar:  # Asumiendo que TreeNode almacena el valor en .value
                nodo_existente = tree_node
                break
        current = current.next
    
    if not nodo_existente:
        # Crear un nuevo árbol para este lugar
        nodo_raiz = TreeNode(lugar)  # El nodo raíz solo almacena el lugar
        cola_comentarios.enqueue(nodo_raiz)
        
        # Crear un nodo hijo con el comentario y el usuario
        nodo_comentario = TreeNode(comentario)
        nodo_comentario.usuario = usuario
        
        # Agregar el comentario como hijo del lugar
        nodo_raiz.agregar_hijo(nodo_comentario)
    else:
        # Agregar el comentario como hijo del lugar existente
        nodo_comentario = TreeNode(comentario)
        nodo_comentario.usuario = usuario
        nodo_existente.agregar_hijo(nodo_comentario)

def seleccionar_nodo(seleccionado):
    pass

def responder_a_nodo(respuesta):
    pass