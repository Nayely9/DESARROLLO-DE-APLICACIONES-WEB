import mysql.connector

def conectar_mysql():
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="clinica",
        port=3307
    )
    return conexion