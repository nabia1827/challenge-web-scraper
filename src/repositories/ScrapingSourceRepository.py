from src.database.db_sql import get_connection

def get_source_url(source_id):
    conexion = get_connection()
    query = "EXEC sp_PyGetSourceUrl ?"
    cursor = conexion.cursor()

    try:        
        cursor.execute(query,(source_id))
        result= cursor.fetchval()
        conexion.commit()
        return result

    except Exception as e:
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()