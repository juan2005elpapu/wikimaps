from DB import create_connection

def obtener_usuarios():
    conn = create_connection("..\wikimaps.db")
    print(create_connection)
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users;")
        users = cursor.fetchall()
        conn.close()
        return users
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []
