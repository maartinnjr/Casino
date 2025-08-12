import mysql.connector
from mysql.connector import Error

# ===================================================================================
# SCRIPT DE PYTHON PARA VACIAR DATOS DEL CASINO (PARA DEMOSTRACIONES)
# ===================================================================================
#
# Este script se conecta a la base de datos de Railway y ejecuta los comandos
# SQL para borrar todos los datos de usuarios, historiales y transacciones.
#
# CÓMO USARLO:
# 1. Asegúrate de que las credenciales en 'db_config' son las correctas.
# 2. Guarda este archivo como "vaciar_db.py" en la misma carpeta que tu juego.
# 3. Ejecútalo desde tu terminal con el comando: python vaciar_db.py
#

# --- CONFIGURACIÓN DE LA CONEXIÓN (COPIADA DE TU JUEGO) ---
db_config = {
    'host': 'shinkansen.proxy.rlwy.net',
    'user': 'root',
    'password': 'wEWnpjufrkFVWvhNcMnoKCPXtfJEgrMD',
    'database': 'railway', # Asegúrate que el nombre de la DB sea el correcto
    'port': 53316
}

def vaciar_base_de_datos():
    """Se conecta a la DB y vacía las tablas de datos de usuario."""
    
    connection = None  # Inicializa la variable de conexión
    try:
        print("🔌 Conectando a la base de datos de Railway...")
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        print("✅ Conexión exitosa.")

        # Lista de comandos SQL a ejecutar (tomados de tu script)
        comandos = [
            "SET FOREIGN_KEY_CHECKS = 0;",
            "TRUNCATE TABLE `historial_partidas`;",
            "TRUNCATE TABLE `transacciones`;",
            "TRUNCATE TABLE `canjes_dulces`;",
            "TRUNCATE TABLE `usuarios`;",
            "SET FOREIGN_KEY_CHECKS = 1;"
        ]

        print("\n🚀 Empezando el proceso de vaciado...")
        
        for comando in comandos:
            # Se usa 'multi=True' si un comando tiene varias sentencias,
            # pero es más seguro ejecutar uno por uno.
            if 'TRUNCATE' in comando:
                tabla = comando.split('`')[1]
                print(f"   - Vaciando la tabla: {tabla}...")
            
            cursor.execute(comando)
        
        connection.commit() # Confirma todos los cambios
        
        print("\n🎉 ¡Éxito! La base de datos ha sido limpiada para la demostración.")

    except Error as e:
        print(f"❌ Error al conectar o ejecutar el script: {e}")
        if connection and connection.is_connected():
            connection.rollback() # Revierte los cambios si algo falló
            print("   - Se han revertido los cambios.")

    finally:
        # Se asegura de que la conexión siempre se cierre
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Conexión a la base de datos cerrada.")

# --- Punto de entrada para ejecutar el script ---
if __name__ == "__main__":
    # Pregunta de seguridad para evitar ejecuciones accidentales
    confirmacion = input("❓ ¿Está seguro de que desea BORRAR todos los usuarios, historiales y transacciones? (s/n): ")
    if confirmacion.lower() == 's':
        vaciar_base_de_datos()
    else:
        print("🚫 Operación cancelada.")
