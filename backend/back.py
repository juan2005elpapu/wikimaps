import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class Nodo:
    def __init__(self, valor):
        self.valor = valor
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

    def mostrar(self, parent="", nivel=0):
        arista = tree.insert(parent, "end", text=" " * (nivel * 2) + str(self.valor), open=True)
        if self.hijo:
            self.hijo.mostrar(arista, nivel + 1)
        if self.hermano:
            self.hermano.mostrar(parent, nivel)

raices = []
nodo_seleccionado = None

def actualizar_interfaz():
    limpiar_treeview()
    for raiz in raices:
        raiz.mostrar()

def limpiar_treeview():
    for vertices in tree.get_children():
        tree.delete(vertices)

def agregar_comentario():
    comentario = simpledialog.askstring("Nuevo Comentario", "Ingrese su comentario:")
    if comentario:
        raices.append(Nodo(comentario))
        actualizar_interfaz()

def seleccionar_nodo(event):
    global nodo_seleccionado
    seleccionado = tree.selection()
    if seleccionado:
        valor = tree.item(seleccionado, "text").strip()
        for raiz in raices:
            nodo_seleccionado = raiz.buscar_nodo(valor)
            if nodo_seleccionado:
                break  
            else:
                nodo_seleccionado = None 

            

def responder_a_nodo():
    global nodo_seleccionado
    if nodo_seleccionado:
        respuesta = simpledialog.askstring("Responder", "Ingrese su respuesta:")
        if respuesta:
            nodo_seleccionado.agregar_hijo(Nodo(respuesta))
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

actualizar_interfaz()
root.mainloop()
