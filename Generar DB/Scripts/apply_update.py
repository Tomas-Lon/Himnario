import sqlite3, json

conn = sqlite3.connect("himnario.db")
c = conn.cursor()

with open("update.json", encoding="utf-8") as f:
    data = json.load(f)

for h in data["hymnsToAdd"]:
    c.execute("""
        INSERT INTO hymns (numero, title, lyrics, note)
        VALUES (?, ?, ?, ?)
    """, (h["numero"], h["title"], h["lyrics"], h.get("musical_key","")))

for h in data["hymnsToUpdate"]:
    c.execute("""
        UPDATE hymns
        SET numero=?, title=?, lyrics=?, note=?
        WHERE id=?
    """, (h["numero"], h["title"], h["lyrics"], h.get("musical_key",""), h["id"]))

for i in data["hymnIdsToDelete"]:
    c.execute("DELETE FROM hymns WHERE id=?", (i,))

conn.commit()
conn.close()
print("DB actualizada")
