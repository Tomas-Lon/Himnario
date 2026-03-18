def parse_hymn_txt(path):
    hymns = {}

    with open(path, encoding="utf-8") as f:
        blocks = [b.strip() for b in f.read().split('---') if b.strip()]

    for b in blocks:
        lines = b.splitlines()
        hymn = {}
        current = None
        lyrics = []

        for line in lines:
            if ':' in line and not line.startswith(' '):
                key, val = line.split(':', 1)
                key = key.strip()
                val = val.strip()

                if key == "lyrics":
                    current = "lyrics"
                    lyrics = []
                else:
                    current = None
                    hymn[key] = int(val) if key in ("id", "numero") else val
            else:
                if current == "lyrics":
                    lyrics.append(line)

        hymn["lyrics"] = "\n".join(lyrics).strip()
        hymns[hymn["id"]] = hymn

    return hymns
