import subprocess
import sys
import os

SCRIPT_DIR = os.path.join(os.path.dirname(__file__), 'scripts')

def run_script(script_name):
    script_path = os.path.join(SCRIPT_DIR, script_name)
    print(f'\n--- Ejecutando: {script_name} ---')
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print('Error:', result.stderr)

if __name__ == '__main__':
    print('='*80)
    print('PIPELINE HIMNARIO AUTOMATIZADO')
    print('='*80)
    # Paso 1: Parsear TXT Word
    print("[1/6] Parseando archivo TXT exportado de Word...")
    pre_dir = os.path.join(os.path.dirname(__file__), 'pre-proceso')
    archivos_txt = [f for f in os.listdir(pre_dir) if f.endswith('.txt')]
    if not archivos_txt:
        print('⚠ No se encontró archivo .txt en pre-proceso/')
        sys.exit(1)
    archivo_input = archivos_txt[0]
    subprocess.run([
        sys.executable,
        os.path.join(SCRIPT_DIR, "parsear_txt_word.py"),
        archivo_input
    ], check=True)
    # 2. Normalizar formato y capitalización
    run_script('procesar_formato.py')
    # 3. Limpiar duplicaciones
    run_script('limpiar_duplicaciones.py')
    # 4. (Opcional) Ordenar alfabéticamente
    run_script('ordenar_alfabetico.py')
    # 5. Generar JSON Holyrics
    run_script('generar_json_holyrics.py')
    # 6. Generar DOCX imprimible
    run_script('crear_himnario.py')
    # 7. Generar PDF profesional
    run_script('generar_pdf_himnario.py')
    # Generar reporte final
    post_dir = os.path.join(os.path.dirname(__file__), 'post-proceso')
    reporte_path = os.path.join(post_dir, 'REPORTE_PIPELINE.txt')
    with open(reporte_path, 'w', encoding='utf-8') as f:
        f.write('='*80 + '\n')
        f.write('REPORTE FINAL DEL PIPELINE HIMNARIO\n')
        f.write('='*80 + '\n\n')
        f.write('Archivos generados:\n')
        for nombre in [
            'Himnario_Extraido.txt',
            'Himnario_Limpio_Final.txt',
            'Indice_Alfabetico_Final.txt',
            'REPORTE_CAMBIOS.txt',
            'REPORTE_REORDENAMIENTO.txt',
            'Himnario_Completo_Holyrics.json',
        ]:
            ruta = os.path.join(post_dir, nombre)
            existe = os.path.exists(ruta)
            f.write(f"- {nombre}: {'OK' if existe else 'NO GENERADO'}\n")
        # Buscar DOCX generado
        docx_files = [fn for fn in os.listdir(post_dir) if fn.lower().endswith('.docx')]
        for docx in docx_files:
            f.write(f"- {docx}: OK\n")
        f.write('\nResumen:\n')
        # Contar himnos
        try:
            with open(os.path.join(post_dir, 'Himnario_Limpio_Final.txt'), 'r', encoding='utf-8') as h:
                contenido = h.read()
                total = contenido.count('\n\n')
                f.write(f"Total de himnos procesados: {total}\n")
        except Exception:
            f.write("Total de himnos procesados: No disponible\n")
        # JSON Holyrics
        try:
            import json
            with open(os.path.join(post_dir, 'Himnario_Completo_Holyrics.json'), 'r', encoding='utf-8') as j:
                datos = json.load(j)
                f.write(f"Total de himnos en JSON Holyrics: {len(datos)}\n")
        except Exception:
            f.write("Total de himnos en JSON Holyrics: No disponible\n")
        f.write('\n¡Pipeline ejecutado correctamente!\n')
        f.write('='*80 + '\n')
    print(f'\nOK Pipeline completo. Archivos generados en post-proceso/.')
    print(f'OK Reporte generado: {reporte_path}')
    print('='*80)
