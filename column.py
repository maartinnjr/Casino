import mysql.connector
from mysql.connector import errorcode

# --- CONFIGURACIÓN DE LA CONEXIÓN A LA BASE DE DATOS MYSQL ---
# Asegúrate de que estos datos son correctos
db_config = {
    'host': 'shinkansen.proxy.rlwy.net',
    'user': 'root',
    'password': 'wEWnpjufrkFVWvhNcMnoKCPXtfJEgrMD',
    'database': 'railway',
    'port': 53316
}

def agregar_juego_coinflip():
    """
    Se conecta a la base de datos e inserta el juego 'Coinflip'
    en la tabla 'juegos' si no existe ya.
    """
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Datos del nuevo juego
        id_juego = 4
        nombre_juego = "Coinflip"
        descripcion = "Apuesta a cara o sello y duplica tu monto."
        apuesta_minima = 100

        # Verificar si el juego ya existe para no duplicarlo
        query_verificar = "SELECT id_juego FROM juegos WHERE id_juego = %s OR nombre_juego = %s"
        cursor.execute(query_verificar, (id_juego, nombre_juego))
        
        if cursor.fetchone():
            print(f"El juego '{nombre_juego}' con ID {id_juego} ya existe en la base de datos.")
        else:
            # Si no existe, insertarlo
            query_insertar = """
                INSERT INTO juegos (id_juego, nombre_juego, descripcion, apuesta_minima) 
                VALUES (%s, %s, %s, %s)
            """
            datos_juego = (id_juego, nombre_juego, descripcion, apuesta_minima)
            
            cursor.execute(query_insertar, datos_juego)
            conn.commit()
            print(f"¡Éxito! El juego '{nombre_juego}' ha sido añadido a la base de datos con ID {id_juego}.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Algo está mal con tu usuario o contraseña de la base de datos.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: La base de datos no existe.")
        else:
            print(f"Ocurrió un error: {err}")
    finally:
        # Cerrar la conexión
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexión a la base de datos cerrada.")

# --- Ejecutar la función ---
if __name__ == "__main__":
    agregar_juego_coinflip()
