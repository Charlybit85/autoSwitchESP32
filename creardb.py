import sqlite3
conn = sqlite3.connect('usuarios.db')
conn.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             usuario TEXT UNIQUE NOT NULL,
             password_hash TEXT NOT NULL)''')
conn.commit()
conn.close()
print("Base de datos y tabla 'usuarios' creadas exitosamente")