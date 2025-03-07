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

def actualizar_interfaz():
    limpiar_treeview()
    current = cola_comentarios.head
    while current:
        current.value.mostrar()  
        current = current.next

def limpiar_treeview():
    for vertices in tree.get_children():
        tree.delete(vertices)

def agregar_comentario():
    comentario = simpledialog.askstring("Nuevo Comentario", "Ingrese su comentario:")
    if comentario:
        nodo = Node(comentario, usuario)  
        cola_comentarios.enqueue(nodo)  
        actualizar_interfaz()

def seleccionar_nodo(event):
    global nodo_seleccionado
    seleccionado = tree.selection()
    if seleccionado:
        if "usuario" in tree.item(seleccionado, "tags"):  
            return
        valor = tree.item(seleccionado, "text").strip()
        current = cola_comentarios.head
        while current:
            nodo_seleccionado = current.value.buscar_nodo(valor)
            if nodo_seleccionado:
                break
            current = current.next
        else:
            nodo_seleccionado = None

def responder_a_nodo():
    global nodo_seleccionado
    if nodo_seleccionado:
        respuesta = simpledialog.askstring("Responder", "Ingrese su respuesta:")
        if respuesta:
            respuesta_nodo = Node(respuesta, usuario) 
            nodo_seleccionado.agregar_hijo(respuesta_nodo)  
            actualizar_interfaz()
    else:
        messagebox.showwarning("Atención", "Seleccione un comentario primero.")

root = tk.Tk()
root.title("Sistema de Comentarios")
root.geometry("500x500")

frame_botones = tk.Frame(root)
frame_botones.pack(pady=5)

tk.Button(frame_botones, text="Hacer un Comentario", command=agregar_comentario).pack(side="left", padx=5)
tk.Button(frame_botones, text="Responder", command=responder_a_nodo).pack(side="left", padx=5)

tree = ttk.Treeview(root)
tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", seleccionar_nodo)

tree.tag_configure("usuario", background="#e0e0e0", foreground="black")  
actualizar_interfaz()
root.mainloop()