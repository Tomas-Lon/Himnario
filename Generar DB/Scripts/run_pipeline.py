import subprocess
import sys
import os

# ---------- CONFIGURACIÓN ----------
SCRIPTS = [
    {
        "name": "Exportar DB a TXT",
        "script": "export_db_to_txt.py",
        "outputs": ["db.txt"]
    },
    {
        "name": "Normalizar TXT de Holyrics",
        "script": "holyrics_to_updated_txt.py",
        "outputs": ["updated.txt"]
    },
    {
        "name": "Comparar TXT y generar JSON",
        "script": "compare_txts.py",
        "outputs": ["update.json"]
    }
]

APPLY_SCRIPT = "apply_update.py"  # Paso final (opcional, peligroso)

# ---------- UTILIDADES ----------
def run_script(script_name):
    print(f"\n▶ Ejecutando: {script_name}")
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("❌ Error al ejecutar el script")
        print(result.stderr)
        sys.exit(1)

    print(result.stdout.strip())

def check_outputs(files):
    for f in files:
        if not os.path.exists(f):
            print(f"❌ Archivo esperado no encontrado: {f}")
            sys.exit(1)

# ---------- PIPELINE ----------
def main():
    print("\n=== PIPELINE DE ACTUALIZACIÓN DEL HIMNARIO ===")

    for step in SCRIPTS:
        if not os.path.exists(step["script"]):
            print(f"❌ Script no encontrado: {step['script']}")
            sys.exit(1)

        run_script(step["script"])
        check_outputs(step["outputs"])

    print("\n✅ Pipeline completado correctamente")
    print("📄 Revisa 'update.json' antes de aplicar cambios a la DB")

    # Confirmación explícita para tocar la DB
    confirm = input("\n¿Deseas aplicar los cambios a la DB? (SI / NO): ").strip().upper()
    if confirm == "SI":
        if not os.path.exists(APPLY_SCRIPT):
            print(f"❌ Script no encontrado: {APPLY_SCRIPT}")
            sys.exit(1)
        run_script(APPLY_SCRIPT)
        print("🗄️ Cambios aplicados a la DB")
    else:
        print("🛑 Cambios NO aplicados (modo seguro)")

if __name__ == "__main__":
    main()
