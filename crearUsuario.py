import sqlite3
import sys
from getpass import getpass
from werkzeug.security import generate_password_hash
usuario = input("Ingrese el nombre de usuario: ").strip()
if not usuario:
    sys.exit("El nombre de usuario no puede estar vacío.")
password = getpass("Ingrese la contraseña: ")
if len(password) < 8:
    sys.exit("La contraseña debe tener al menos 8 caracteres.")
if password != getpass("Confirme la contraseña: "):
    sys.exit("Las contraseñas no coinciden.")
conn = sqlite3.connect('usuarios.db')
try:
    # Guardamos el usuario y la contraseña hasheada en la base de datos
    conn.execute('INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)', (usuario, generate_password_hash(password))) 
    conn.commit()
    print(f"Usuario '{usuario}' creado exitosamente.")
except sqlite3.IntegrityError:
    print(f"Error: El usuario '{usuario}' ya existe.")
finally:
    conn.close()