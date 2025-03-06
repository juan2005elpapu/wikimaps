import tkinter as tk
from tkinter import ttk
from usuarios import obtener_usuarios

def display():
    usuarios = obtener_usuarios()

    root = tk.Tk()
    root.title("Lista de Usuarios")

    tree = ttk.Treeview(root, columns=("ID", "Nombre"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.pack(fill="both", expand=True)

    for user in usuarios:
        tree.insert("", "end", values=user)

    root.mainloop()

if __name__ == "__main__":
    display()