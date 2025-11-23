import os
import django
from django.db import connection

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowbar_project.settings')
django.setup()

def forzar_arreglo():
    print("--- INICIANDO REPARACIÓN FORZADA DE LA BASE DE DATOS ---")
    with connection.cursor() as cursor:
        # 1. Verificar y arreglar 'detalle_pedido'
        print("\n1. Verificando tabla 'detalle_pedido'...")
        try:
            # Intentamos seleccionar la columna 'id' para ver si existe
            cursor.execute("SELECT id FROM detalle_pedido LIMIT 1")
            print(" -> La columna 'id' YA EXISTE en 'detalle_pedido'.")
        except Exception as e:
            print(f" -> La columna 'id' NO existe. Intentando agregarla... ({e})")
            try:
                # Si falla la selección, intentamos agregar la columna
                # Primero intentamos borrar la PK existente si es compuesta
                try:
                    cursor.execute("ALTER TABLE detalle_pedido DROP PRIMARY KEY")
                    print(" -> Clave primaria anterior eliminada (si existía).")
                except Exception as e_pk:
                    print(f" -> Aviso al borrar PK: {e_pk}")

                # Agregamos la columna 'id'
                cursor.execute("ALTER TABLE detalle_pedido ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")
                print("✅ ¡ÉXITO! Columna 'id' agregada a 'detalle_pedido'.")
            except Exception as e_add:
                print(f"❌ ERROR al agregar columna 'id' a 'detalle_pedido': {e_add}")

        # 2. Verificar y arreglar 'asignado'
        print("\n2. Verificando tabla 'asignado'...")
        try:
            cursor.execute("SELECT id FROM asignado LIMIT 1")
            print(" -> La columna 'id' YA EXISTE en 'asignado'.")
        except Exception as e:
            print(f" -> La columna 'id' NO existe. Intentando agregarla... ({e})")
            try:
                try:
                    cursor.execute("ALTER TABLE asignado DROP PRIMARY KEY")
                    print(" -> Clave primaria anterior eliminada (si existía).")
                except Exception as e_pk:
                    print(f" -> Aviso al borrar PK: {e_pk}")

                cursor.execute("ALTER TABLE asignado ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST")
                print("✅ ¡ÉXITO! Columna 'id' agregada a 'asignado'.")
            except Exception as e_add:
                print(f"❌ ERROR al agregar columna 'id' a 'asignado': {e_add}")

    print("\n--- REPARACIÓN FINALIZADA ---")

if __name__ == '__main__':
    forzar_arreglo()