# Pipeline de Actualización del Himnario

Este proyecto permite comparar el estado actual del himnario almacenado en SQLite
con un archivo TXT exportado desde Holyrics, detectar cambios y actualizar la base
de datos de forma segura y controlada.

---

## 🎯 Objetivo

- Detectar himnos nuevos
- Detectar himnos modificados
- Detectar himnos eliminados
- Evitar revisión manual de cientos/miles de himnos
- Mantener la DB de la app consistente

---

## 🧭 Flujo de trabajo

himnario.db
│
▼
export_db_to_txt.py
│
▼
db.txt
│
│ TomasDB_Holyrics.txt
│ │
│ ▼
│ holyrics_to_updated_txt.py
│ │
└──────────────► updated.txt
│
▼
compare_txts.py
│
▼
update.json
│
▼
apply_update.py
│
▼
himnario.db

---

## 📂 Archivos principales

### Base de datos
- `himnario.db` → DB SQLite usada por la app

### Archivos TXT
- `db.txt` → Export normalizado de la DB (NO editar)
- `TomasDB_Holyrics.txt` → TXT exportado desde Holyrics (entrada)
- `updated.txt` → TXT de Holyrics normalizado
- `update.json` → Cambios detectados

---

## 🧩 Scripts

| Script | Función |
|------|-------|
| `export_db_to_txt.py` | Exporta la DB a TXT normalizado |
| `holyrics_to_updated_txt.py` | Convierte TXT de Holyrics a formato normal |
| `parse_txt.py` | Parser común para TXT normalizado |
| `compare_txts.py` | Genera `update.json` |
| `apply_update.py` | Aplica cambios a SQLite |
| `run_pipeline.py` | Orquesta todo el proceso |

---

## ▶ Ejecución recomendada

```bash
python run_pipeline.py