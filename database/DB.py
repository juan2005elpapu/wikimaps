import sqlite3

def create_connection(db_file):
    """Crea una conexión a la base de datos SQLite especificada por db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conectado a SQLite versión: {sqlite3.sqlite_version}")
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return conn

def create_table(conn):
    """Crea una tabla 'comments' en la base de datos si no existe."""
    try:
        sql_create_comments_table = '''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY,
            comment TEXT NOT NULL,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES comments (id)
        );
        '''
        cursor = conn.cursor()
        cursor.execute(sql_create_comments_table)
        conn.commit()
        print("Tabla 'comments' creada exitosamente (o ya existía).")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")

if __name__ == '__main__':
    database = "wikimaps.db"  # Esto creará el archivo wikimaps.db en la carpeta actual
    conn = create_connection(database)
    if conn:
        create_table(conn)
        conn.close()