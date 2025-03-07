import os
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dataStructures.fifoQueue import FifoQueue
from nodes.node import Node
from mapApp import get_current_user

cola_comentarios = FifoQueue()
nodo_seleccionado = None
usuario = get_current_user()


#lugar es el nodo seleccionado en el mapa
def mostrar_arbol(lugar):
        lugar.mostrar()

#se le pasa la raiz que es el nodo seleccionado en el mapa y el valor que es el comentario, si no existe esa raiz se crea el arbol
#de lo contrario se le pone el comentario como un hijo 
def agregar_comentario(lugar, comentario):
    nodo_raiz = cola_comentarios.head
    while nodo_raiz:
        if nodo_raiz.valor == lugar:
            break
        nodo_raiz = nodo_raiz.hermano
    
    if not nodo_raiz:
        nodo_raiz = Node(lugar,usuario)
        cola_comentarios.enqueue(nodo_raiz)  

    if comentario:
        nuevo_comentario = Node(comentario, "Usuario")  
        nodo_raiz.agregar_hijo(nuevo_comentario)  

#se le pasa el valor del comentario seleccionado y busca de quien es hijo
def seleccionar_nodo(seleccionado):
    global nodo_seleccionado
    if seleccionado:
        valor = seleccionado
        current = cola_comentarios.head
        while current:
            nodo_seleccionado = current.value.buscar_nodo(valor)
            if nodo_seleccionado:
                break
            current = current.next
        else:
            nodo_seleccionado = None

#agrega la respuesta como un hijo del nodo seleccionado
def responder_a_nodo(respuesta):
    global nodo_seleccionado
    if nodo_seleccionado:
        if respuesta:
            respuesta_nodo = Node(respuesta, usuario) 
            nodo_seleccionado.agregar_hijo(respuesta_nodo)  
            "actualizar_interfaz()"
    else:
        print("Atención", "Seleccione un comentario primero.")