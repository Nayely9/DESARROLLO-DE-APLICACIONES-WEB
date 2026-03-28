from conexion.conexion import conectar_mysql

def registrar_asignacion(m_id, p_id, cant, fecha):
    """
    Registra una nueva entrega en la tabla medicamento_paciente 
    y actualiza el stock en la tabla medicamento.
    """
    db = conectar_mysql()
    cursor = db.cursor(dictionary=True)
    try:
        # 1. Verificar si hay stock suficiente antes de procesar
        cursor.execute("SELECT stock FROM medicamento WHERE medicamento_id = %s", (m_id,))
        resultado = cursor.fetchone()
        
        if resultado and resultado['stock'] >= int(cant):
            # 2. Insertar el registro usando los nombres de tu base de datos
            query_insert = """
                INSERT INTO medicamento_paciente (medicamento_id, paciente_id, cantidad, fecha_asignacion) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_insert, (m_id, p_id, cant, fecha))
            
            # 3. Restar la cantidad del inventario
            query_update = "UPDATE medicamento SET stock = stock - %s WHERE medicamento_id = %s"
            cursor.execute(query_update, (cant, m_id))
            
            db.commit()
            return True
        else:
            # No hay stock suficiente
            return False
            
    except Exception as e:
        print(f"Error al registrar la asignación: {e}")
        db.rollback() # Revierte cambios si hubo un error
        return False
    finally:
        db.close()

def listar_asignaciones():
    """
    Obtiene el historial de entregas uniendo las tablas para mostrar 
    nombres en lugar de solo IDs.
    """
    db = conectar_mysql()
    cursor = db.cursor(dictionary=True)
    try:
        # Usamos JOIN para traer el nombre del medicamento y del paciente
        query = """
            SELECT 
                mp.asignacion_id, 
                m.nombre AS medicamento, 
                p.nombre AS paciente, 
                mp.cantidad, 
                mp.fecha_asignacion 
            FROM medicamento_paciente mp
            JOIN medicamento m ON mp.medicamento_id = m.medicamento_id
            JOIN paciente p ON mp.paciente_id = p.paciente_id
            ORDER BY mp.fecha_asignacion DESC
        """
        cursor.execute(query)
        asignaciones = cursor.fetchall()
        return asignaciones if asignaciones else []
    except Exception as e:
        print(f"Error al listar asignaciones: {e}")
        return []
    finally:
        db.close()