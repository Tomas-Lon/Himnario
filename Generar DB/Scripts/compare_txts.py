from otri.parse_holyrics_txt import parse_hymn_txt
from match_hymns import build_title_index, resolve_hymn_id
import json

FIELDS_STRICT = ["numero", "title", "lyrics"]
FIELDS_OPTIONAL = ["musical_key"]

def has_value(v):
    return v is not None and str(v).strip() != ""

db = parse_hymn_txt("db.txt")
upd = parse_hymn_txt("updated.txt")

title_index, collisions = build_title_index(db)

if collisions:
    print("⚠️ Títulos duplicados en DB (revisar manualmente):")
    for t, ids in collisions.items():
        print(f"  '{t}' → IDs {ids}")

to_add = []
to_update = []
matched_ids = set()

for _, new in upd.items():
    resolved_id = resolve_hymn_id(new, db, title_index)

    # ➕ Himno nuevo
    if resolved_id is None:
        to_add.append(new)
        continue

    matched_ids.add(resolved_id)
    old = db[resolved_id]

    changed = False

    # Campos obligatorios
    for f in FIELDS_STRICT:
        if old.get(f, "") != new.get(f, ""):
            changed = True

    # Campos opcionales (solo si vienen informados)
    for f in FIELDS_OPTIONAL:
        if has_value(new.get(f)) and old.get(f, "") != new.get(f):
            changed = True

    if changed:
        new["id"] = resolved_id   # 🔒 forzar ID correcto
        to_update.append(new)

# ➖ Himnos eliminados
to_delete = [i for i in db.keys() if i not in matched_ids]

with open("update.json", "w", encoding="utf-8") as f:
    json.dump({
        "hymnsToAdd": to_add,
        "hymnsToUpdate": to_update,
        "hymnIdsToDelete": to_delete
    }, f, indent=2, ensure_ascii=False)

print("update.json generado (matching por título + nota opcional)")
