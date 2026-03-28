import mysql.connector

def conectar_mysql():
    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="gestion_clinica",
            port=33060
        )
        return conexion
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None