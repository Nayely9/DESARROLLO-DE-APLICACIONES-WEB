from conexion.conexion import conectar_mysql

def insertar_paciente(nombre, email):
    db = conectar_mysql()
    cursor = db.cursor()
    cursor.execute("INSERT INTO paciente (nombre, email) VALUES (%s, %s)", (nombre, email))
    db.commit()
    db.close()
    
def listar_pacientes():
    db = conectar_mysql()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM paciente")
    res = cursor.fetchall()
    db.close()
    return res if res else []