import sqlite3

def conectar():
    conexion = sqlite3.connect("clinica.db")
    conexion.row_factory = sqlite3.Row
    return conexion

def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        proveedor TEXT NOT NULL
    )
    """)

    conexion.commit()
    conexion.close()