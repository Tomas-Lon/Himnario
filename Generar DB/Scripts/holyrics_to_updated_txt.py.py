import re

INPUT = "TomasDB_Holyrics.txt"
OUTPUT = "updated.txt"

def parse_holyrics(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r'\n=+\n', content)
    hymns = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.splitlines()
        title = ""
        musical_key = None
        lyrics = []

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith("Título:"):
                title = line.replace("Título:", "").strip()

            elif line.startswith("Nota:"):
                musical_key = line.replace("Nota:", "").strip()

            elif line == "":
                lyrics = lines[i+1:]
                break

            i += 1

        hymns.append({
            "title": title,
            "musical_key": musical_key,
            "lyrics": "\n".join(lyrics).strip()
        })

    return hymns


def write_updated_txt(hymns):
    with open(OUTPUT, "w", encoding="utf-8") as f:
        for idx, h in enumerate(hymns, start=1):
            f.write("---\n")
            f.write(f"id: {idx}\n")        # ID temporal (se resuelve después)
            f.write(f"numero: {idx}\n")
            f.write(f"title: {h['title']}\n")

            # ⚠️ SOLO escribir musical_key si existe
            if h.get("musical_key"):
                f.write(f"musical_key: {h['musical_key']}\n")

            f.write("lyrics:\n")
            f.write(h["lyrics"] + "\n")


if __name__ == "__main__":
    hymns = parse_holyrics(INPUT)
    write_updated_txt(hymns)
    print(f"{len(hymns)} himnos normalizados desde Holyrics")
