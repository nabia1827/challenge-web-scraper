from src.database.db_sql import get_connection


def get_status_token(user_id,token):
    conexion = get_connection()
    query = "exec sp_PyVerifyRefreshToken ?,?"
    cursor = conexion.cursor()
    try:
        cursor.execute(query,(
            user_id,
            token
        ))
        result= cursor.fetchval()
        conexion.commit()
        return result
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()

def set_token(user_id,token):
    conexion = get_connection()
    query = "exec sp_PyInsertTokenPython ?,?"
    cursor = conexion.cursor()
    try:
        cursor.execute(query,(
            user_id,
            token
        ))
        conexion.commit()

    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        conexion.rollback()
    finally:
        cursor.close()
        conexion.close()