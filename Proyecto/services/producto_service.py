from conexion.conexion import conectar_mysql

def listar_medicamentos():
    db = conectar_mysql()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT medicamento_id, nombre, precio, stock FROM medicamento")
    res = cursor.fetchall()
    db.close()
    return res

def obtener_medicamento(id):
    db = conectar_mysql()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM medicamento WHERE medicamento_id = %s", (id,))
    res = cursor.fetchone()
    db.close()
    return res

def insertar_producto(nombre, precio, stock):
    db = conectar_mysql()
    cursor = db.cursor()
    cursor.execute("INSERT INTO medicamento (nombre, precio, stock) VALUES (%s, %s, %s)", (nombre, precio, stock))
    db.commit()
    db.close()

def actualizar_producto(id, nombre, precio, stock):
    db = conectar_mysql()
    cursor = db.cursor()
    cursor.execute("UPDATE medicamento SET nombre=%s, precio=%s, stock=%s WHERE medicamento_id=%s", (nombre, precio, stock, id))
    db.commit()
    db.close()

def eliminar_medicamento(id):
    db = conectar_mysql()
    cursor = db.cursor()
    cursor.execute("DELETE FROM medicamento WHERE medicamento_id = %s", (id,))
    db.commit()
    db.close()