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
        # Crear la tabla users si no existe, ahora con columna email
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            );
        ''')
        conn.commit()
        # Verificar si la tabla está vacía
        cursor.execute("SELECT COUNT(*) FROM users;")
        count = cursor.fetchone()[0]
        if count == 0:
            # Insertar registros dummy
            users_data = [
                ("Alice", "password1", "alice@example.com"),
                ("Bob", "mypassword", "bob@example.com"),
                ("Charlie", "secret123", "charlie@example.com")
            ]
            for name, plain, email in users_data:
                encrypter = Encrypter(plain)
                encrypted = encrypter.RSA_Encrypt()
                cursor.execute("INSERT INTO users (name, password, email) VALUES (?, ?, ?)", 
                               (name, encrypted, email))
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
        cursor.execute("SELECT id, name, password, email FROM users;")
        users = cursor.fetchall()
        # Desencriptar las contraseñas
        decrypted_users = []
        # La contraseña en el constructor no afecta la decriptación (se utilizan los mismos parámetros RSA)
        encrypter = Encrypter('')
        for user in users:
            user_id, name, encrypted_password, email = user
            decrypted_password = encrypter.RSA_Decrypt(encrypted_password)
            decrypted_users.append((user_id, name, decrypted_password, email))
        return decrypted_users
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

def verificar_usuario(username, password):
    db_path = os.path.join(os.path.dirname(__file__), "..", "wikimaps.db")
    conn = create_connection(db_path)
    if not conn:
        return False, "Error de conexión a la base de datos"
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE name = ?", (username,))
        result = cursor.fetchone()
        
        if not result:
            return False, "Usuario no encontrado"
            
        encrypted_password = result[0]
        encrypter = Encrypter('')
        decrypted_password = encrypter.RSA_Decrypt(encrypted_password)
        
        if decrypted_password == password:
            return True, "Autenticación exitosa"
        else:
            return False, "Contraseña incorrecta"
    except Exception as e:
        print(f"Error al verificar usuario: {e}")
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def usuario_existe(username):
    db_path = os.path.join(os.path.dirname(__file__), "..", "wikimaps.db")
    conn = create_connection(db_path)
    if not conn:
        return True, "Error de conexión a la base de datos"
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE name = ?", (username,))
        count = cursor.fetchone()[0]
        return count > 0, "Usuario ya existe" if count > 0 else "Usuario disponible"
    except Exception as e:
        print(f"Error al verificar existencia de usuario: {e}")
        return True, f"Error: {str(e)}"
    finally:
        conn.close()

def email_existe(email):
    db_path = os.path.join(os.path.dirname(__file__), "..", "wikimaps.db")
    conn = create_connection(db_path)
    if not conn:
        return True, "Error de conexión a la base de datos"
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE email = ?", (email,))
        count = cursor.fetchone()[0]
        return count > 0, "Email ya registrado" if count > 0 else "Email disponible"
    except Exception as e:
        print(f"Error al verificar existencia de email: {e}")
        return True, f"Error: {str(e)}"
    finally:
        conn.close()

def registrar_usuario(username, password, email):
    db_path = os.path.join(os.path.dirname(__file__), "..", "wikimaps.db")
    conn = create_connection(db_path)
    if not conn:
        return False, "Error de conexión a la base de datos"
    
    # Verificar si el usuario ya existe
    existe, mensaje = usuario_existe(username)
    if existe:
        return False, mensaje
    
    # Verificar si el email ya existe
    existe, mensaje = email_existe(email)
    if existe:
        return False, mensaje
    
    try:
        cursor = conn.cursor()
        # Encriptar la contraseña
        encrypter = Encrypter(password)
        encrypted_password = encrypter.RSA_Encrypt()
        
        # Insertar el nuevo usuario
        cursor.execute("INSERT INTO users (name, password, email) VALUES (?, ?, ?)", 
                       (username, encrypted_password, email))
        conn.commit()
        return True, "Usuario registrado exitosamente"
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False, f"Error: {str(e)}"
    finally:
        conn.close()

def drop_users_table():
    # Construimos la ruta absoluta al archivo wikimaps.db
    db_path = os.path.join(os.path.dirname(__file__), "..", "wikimaps.db")
    conn = create_connection(db_path)
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        # Borrar la tabla users si existe
        cursor.execute('DROP TABLE IF EXISTS users;')
        conn.commit()
        print("Tabla 'users' eliminada exitosamente.")
        return True
    except Exception as e:
        print(f"Error al eliminar la tabla users: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    initialize_users()
