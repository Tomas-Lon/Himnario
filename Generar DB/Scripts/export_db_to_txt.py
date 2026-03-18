import sqlite3

DB_PATH = "himnario.db"
OUTPUT = "db.txt"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("""
    SELECT id, numero, title, lyrics, note
    FROM hymns
    ORDER BY numero
""")

rows = c.fetchall()

with open(OUTPUT, "w", encoding="utf-8") as f:
    for r in rows:
        id_, numero, title, lyrics, note = r

        f.write("---\n")
        f.write(f"id: {id_}\n")
        f.write(f"numero: {numero}\n")
        f.write(f"title: {title}\n")
        if note:
            f.write(f"musical_key: {note}\n")
        f.write("lyrics:\n")
        f.write((lyrics or "").strip() + "\n")

conn.close()
print("db.txt generado")
