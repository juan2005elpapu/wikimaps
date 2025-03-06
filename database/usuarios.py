import sqlite3
import os
import sys

# Agregar la ruta para poder importar Encrypter desde rsa_method.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'maps'))
from rsa_method import Encrypter
from DB import create_connection

def initialize_users():
    # Construimos la ruta absoluta al archivo wikimaps.db
    db_path = os.path.join(os.path.dirname(__file__), "..", "wikimaps.db")
    conn = create_connection(db_path)
    if not conn:
        return
    try:
        cursor = conn.cursor()
        # Crear la tabla users si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL
            );
        ''')
        conn.commit()
        # Verificar si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM users;")
        count = cursor.fetchone()[0]
        if count == 0:
            # Insertar registros dummy
            users_data = [
                ("Alice", "password1"),
                ("Bob", "mypassword"),
                ("Charlie", "secret123")
            ]
            for name, plain in users_data:
                encrypter = Encrypter(plain)
                encrypted = encrypter.RSA_Encrypt()
                cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, encrypted))
            conn.commit()
            print("Usuarios insertados exitosamente.")
    except Exception as e:
        print(f"Error en initialize_users: {e}")
    finally:
        conn.close()

def obtener_usuarios():
    db_path = os.path.join(os.path.dirname(__file__), "..", "wikimaps.db")
    conn = create_connection(db_path)
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password FROM users;")
        users = cursor.fetchall()
        # Desencriptar las contraseñas
        decrypted_users = []
        # La contraseña en el constructor no afecta la decriptación (se utilizan los mismos parámetros RSA)
        encrypter = Encrypter('')
        for user in users:
            user_id, name, encrypted_password = user
            decrypted_password = encrypter.RSA_Decrypt(encrypted_password)
            decrypted_users.append((user_id, name, decrypted_password))
        return decrypted_users
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

if __name__ == '__main__':
    initialize_users()
