"""
Script para medir el rendimiento del proceso completo de conversión y consolidación.
Simula el flujo completo de la aplicación con medición de tiempos.
"""

import time
import sys
import os
from pathlib import Path

# Agregar directorio padre para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def measure_conversion_performance():
    """Mide el rendimiento del proceso completo."""
    
    # Importar después de configurar sys.path
    from main import (
        list_input_files, convert_to_pdf, merge_pdfs,
        INPUT_DIR, OUTPUT_DIR, TEMP_DIR, logger,
        cleanup_office_instances, final_pdf_name
    )
    import shutil
    
    print("🚀 MEDICIÓN DE RENDIMIENTO COMPLETO")
    print("=" * 50)
    
    # Preparar directorios
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Obtener archivos
    files = list_input_files()
    if not files:
        print("❌ No hay archivos en data/input")
        return
    
    print(f"📁 Archivos a procesar: {len(files)}")
    total_start = time.perf_counter()
    
    # FASE 1: Conversiones
    print("\n⚡ FASE 1: Conversiones")
    conversion_start = time.perf_counter()
    
    converted = []
    for i, f in enumerate(files, 1):
        file_start = time.perf_counter()
        print(f"   {i}/{len(files)} Procesando: {f.name[:35]}...", end=" ")
        
        result = convert_to_pdf(f)
        file_time = time.perf_counter() - file_start
        
        if result:
            converted.append(result)
            print(f"✅ {file_time:.2f}s")
        else:
            print(f"❌ {file_time:.2f}s")
    
    conversion_time = time.perf_counter() - conversion_start
    print(f"📊 Conversiones completadas: {len(converted)}/{len(files)} en {conversion_time:.2f}s")
    
    if not converted:
        print("❌ No se convirtió ningún archivo")
        return
    
    # FASE 2: Merge
    print("\n🔗 FASE 2: Unión de PDFs")
    merge_start = time.perf_counter()
    
    output_name = final_pdf_name("TEST", "RENDIMIENTO", "OPTIMIZADO")
    output_path = OUTPUT_DIR / output_name
    
    try:
        merge_pdfs(converted, output_path)
        merge_time = time.perf_counter() - merge_start
        
        final_size = output_path.stat().st_size / (1024 * 1024)
        print(f"✅ Merge completado en {merge_time:.2f}s | PDF final: {final_size:.2f} MB")
        
        # Limpiar archivo de prueba
        if output_path.exists():
            output_path.unlink()
            
    except Exception as e:
        merge_time = time.perf_counter() - merge_start
        print(f"❌ Error en merge: {e}")
    
    # FASE 3: Limpieza
    print("\n🧹 FASE 3: Limpieza")
    cleanup_start = time.perf_counter()
    
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
    cleanup_office_instances()
    
    cleanup_time = time.perf_counter() - cleanup_start
    
    # Resumen final
    total_time = time.perf_counter() - total_start
    
    print(f"\n" + "="*50)
    print("📈 RESUMEN DE RENDIMIENTO")
    print("="*50)
    print(f"⏱️  Tiempo de conversiones: {conversion_time:.2f}s ({conversion_time/total_time*100:.1f}%)")
    print(f"⏱️  Tiempo de merge:       {merge_time:.2f}s ({merge_time/total_time*100:.1f}%)")
    print(f"⏱️  Tiempo de limpieza:    {cleanup_time:.3f}s ({cleanup_time/total_time*100:.1f}%)")
    print(f"⏱️  TIEMPO TOTAL:          {total_time:.2f}s")
    print(f"📊 Eficiencia:            {len(converted)}/{len(files)} archivos convertidos")
    
    # Análisis de rendimiento
    if total_time < 10:
        print("🎯 EXCELENTE: Proceso muy rápido")
    elif total_time < 15:
        print("✅ BUENO: Tiempo de proceso aceptable")
    elif total_time < 20:
        print("⚠️  MODERADO: Se puede optimizar más")
    else:
        print("🐌 LENTO: Requiere optimización adicional")
    
    # Archivos más lentos
    print(f"\n💡 Para mejorar aún más el rendimiento:")
    print(f"   • Los archivos Word (.doc) son los más lentos")
    print(f"   • Considera convertir .doc a .docx para mejor rendimiento")
    print(f"   • Los archivos PDF e imágenes son muy rápidos")

if __name__ == "__main__":
    measure_conversion_performance()