"""
EXPORTAR_SQLITE.PY
==================
Genera una base de datos SQLite (himnario.sqlite) lista para apps móviles a partir de Himnario_Limpio_Final.txt.

Uso:
    python scripts/exportar_sqlite.py

Dependencia:
    Solo Python estándar (usa sqlite3)
"""

import os
import re
import sqlite3

# Rutas
post_dir = os.path.join(os.path.dirname(__file__), '..', 'post-proceso')
archivo_txt = os.path.join(post_dir, 'Himnario_Limpio_Final.txt')
archivo_sqlite = os.path.join(post_dir, 'himnario.sqlite')

# Leer himnos
with open(archivo_txt, 'r', encoding='utf-8') as f:
    contenido = f.read()

patron = r'(\d+)\.\s+(.+?)\n((?:(?!\n\d+\.\s).)+)'
himnos = re.findall(patron, contenido, re.DOTALL)

# Crear base de datos
conn = sqlite3.connect(archivo_sqlite)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS himnos (
    numero INTEGER PRIMARY KEY,
    titulo TEXT NOT NULL,
    letra TEXT NOT NULL
)
''')
c.execute('DELETE FROM himnos')

# Insertar himnos
for numero, titulo, letra in himnos:
    c.execute('INSERT INTO himnos (numero, titulo, letra) VALUES (?, ?, ?)', (int(numero), titulo.strip(), letra.strip()))

conn.commit()
conn.close()

print(f'OK Base de datos SQLite generada: {archivo_sqlite}')
