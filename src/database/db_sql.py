from decouple import config
import pyodbc 

def get_connection():
    try:
        server = config('SERVER')
        database = config('DATABASE')
        username = config('USER')
        password = config('PASSWORD')
        
        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        return cnxn
    except Exception as ex:
        print("error", str(ex))
        return ex