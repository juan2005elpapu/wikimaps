import tkinter as tk
from tkinter import ttk
from usuarios import initialize_users, obtener_usuarios

def display():
    # Inicializar usuarios (crea la tabla e inserta registros si es necesario)
    initialize_users()
    usuarios = obtener_usuarios()

    root = tk.Tk()
    root.title("Lista de Usuarios")

    tree = ttk.Treeview(root, columns=("ID", "Nombre", "Contraseña", "Email"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Contraseña", text="Contraseña")
    tree.heading("Email", text="Email")
    tree.pack(fill="both", expand=True)

    for user in usuarios:
        tree.insert("", "end", values=user)

    root.mainloop()

if __name__ == "__main__":
    display()