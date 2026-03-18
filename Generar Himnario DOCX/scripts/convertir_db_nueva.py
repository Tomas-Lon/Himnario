"""
Convierte una base de datos en texto con bloques que inician con "Título:"
al formato esperado por crear_himnario.py (Himnario_Limpio_Final.txt).
"""

from __future__ import annotations

from pathlib import Path
import re


MARCADOR_SIN_LETRA = "[Sin letra en base de datos]"


def extraer_titulo(linea: str) -> str | None:
    """Extrae título soportando: Título, Titulo y T�tulo (carácter dañado)."""
    linea = linea.lstrip("\ufeff")
    # Acepta una variación opcional entre T y tulo: í / i / � / cualquier carácter.
    patron = re.compile(r"^\s*t(?:[íi\uFFFD]|.)?tulo\s*:\s*(.+?)\s*$", re.IGNORECASE)
    m = patron.match(linea)
    if not m:
        return None
    return m.group(1).strip()


def parsear_db(contenido: str):
    himnos = []
    titulo_actual = None
    lineas_actuales = []

    for linea in contenido.splitlines():
        titulo = extraer_titulo(linea)
        if titulo is not None:
            if titulo_actual is not None:
                letra = "\n".join(lineas_actuales).strip()
                himnos.append((titulo_actual, letra))
            titulo_actual = titulo
            lineas_actuales = []
        else:
            if titulo_actual is not None:
                lineas_actuales.append(linea.rstrip())

    # Último himno
    if titulo_actual is not None:
        letra = "\n".join(lineas_actuales).strip()
        himnos.append((titulo_actual, letra))

    return himnos


def main():
    base_dir = Path(__file__).resolve().parents[1]
    entrada = base_dir / "DB_Iglesia_Revison_Isabel.txt"
    post_dir = base_dir / "post-proceso"
    post_dir.mkdir(parents=True, exist_ok=True)

    salida_limpio = post_dir / "Himnario_Limpio_Final.txt"
    salida_extraido = post_dir / "Himnario_Extraido.txt"

    contenido = entrada.read_text(encoding="utf-8")
    himnos = parsear_db(contenido)

    if not himnos:
        raise SystemExit("No se detectaron himnos en la base de datos de entrada.")

    vacios = sum(1 for _, letra in himnos if not letra.strip())

    for salida in (salida_limpio, salida_extraido):
        with salida.open("w", encoding="utf-8", newline="\n") as f:
            for i, (titulo, letra) in enumerate(himnos, start=1):
                f.write(f"{i}. {titulo}\n")
                texto = letra.strip() if letra.strip() else MARCADOR_SIN_LETRA
                f.write(texto + "\n\n")

    print(f"OK Himnos detectados: {len(himnos)}")
    if vacios:
        print(f"OK Himnos sin letra preservados: {vacios}")
    print(f"OK Generado: {salida_limpio}")
    print(f"OK Generado: {salida_extraido}")


if __name__ == "__main__":
    main()
