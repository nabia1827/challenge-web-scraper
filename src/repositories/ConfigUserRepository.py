from src.database.db_sql import get_connection

def get_user(username):
    conexion = get_connection()
    query = "EXEC sp_PyGetUser ?"
    cursor = conexion.cursor()

    try:        
        cursor.execute(query,(username))
        result= cursor.fetchone()

        conexion.commit()
        return result

    except Exception as e:
        conexion.rollback()
        print(f"Error al ejecutar la consulta: {e}")
    finally:
        cursor.close()
        conexion.close()