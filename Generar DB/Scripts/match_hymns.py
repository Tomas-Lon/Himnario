from normalize_title import normalize_title

def build_title_index(hymns: dict):
    """
    Crea un índice:
    normalized_title -> hymn_id
    """
    index = {}
    collisions = {}

    for hymn_id, h in hymns.items():
        norm = normalize_title(h.get("title", ""))

        if norm in index:
            collisions.setdefault(norm, []).append(hymn_id)
        else:
            index[norm] = hymn_id

    return index, collisions

def resolve_hymn_id(hymn, db_hymns, title_index):
    """
    Devuelve:
    - id existente si hay match
    - None si es nuevo
    """
    # 1️⃣ Match directo por ID
    if "id" in hymn and hymn["id"] in db_hymns:
        return hymn["id"]

    # 2️⃣ Match por título normalizado
    norm = normalize_title(hymn.get("title", ""))
    return title_index.get(norm)
