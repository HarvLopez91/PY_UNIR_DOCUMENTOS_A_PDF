"""
Optimizaciones adicionales de rendimiento para el proceso de conversión.
Este script incluye mejoras específicas para minimizar el tiempo de ejecución.
"""

import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

def convert_files_with_parallel_optimization(files: list[Path]) -> tuple[list[Path], float]:
    """
    Convierte archivos con optimizaciones paralelas para tipos compatibles.
    
    Estrategia:
    1. Archivos Office: Secuencial (COM thread-safety)
    2. Imágenes y PDFs: Paralelo (thread-safe)
    
    Returns:
        Tuple con (lista_pdfs_convertidos, tiempo_total_segundos)
    """
    from main import (
        convert_to_pdf, IMAGE_EXTS, PDF_EXTS, WORD_EXTS, EXCEL_EXTS, logger
    )
    
    start_time = time.perf_counter()
    converted = []
    
    # Separar archivos por capacidad de paralelización
    office_files = [f for f in files if f.suffix.lower() in (WORD_EXTS | EXCEL_EXTS)]
    parallel_files = [f for f in files if f.suffix.lower() in (IMAGE_EXTS | PDF_EXTS)]
    
    logger.info(f"📊 Estrategia de conversión: {len(office_files)} Office (secuencial), {len(parallel_files)} otros (paralelo)")
    
    # 1. Procesar archivos paralelos (imágenes y PDFs) - MÁS RÁPIDO
    if parallel_files:
        logger.info("🚀 Iniciando conversiones paralelas...")
        parallel_start = time.perf_counter()
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_file = {
                executor.submit(convert_to_pdf, f): f 
                for f in parallel_files
            }
            
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    if result:
                        converted.append(result)
                        logger.info(f"✅ Paralelo completado: {file_path.name}")
                    else:
                        logger.error(f"❌ Paralelo falló: {file_path.name}")
                except Exception as e:
                    logger.error(f"❌ Error paralelo en {file_path.name}: {e}")
        
        parallel_time = time.perf_counter() - parallel_start
        logger.info(f"⚡ Conversiones paralelas completadas en {parallel_time:.2f}s")
    
    # 2. Procesar archivos Office secuencialmente (COM safety)
    if office_files:
        logger.info("📄 Iniciando conversiones Office secuenciales...")
        office_start = time.perf_counter()
        
        for f in office_files:
            file_start = time.perf_counter()
            result = convert_to_pdf(f)
            file_time = time.perf_counter() - file_start
            
            if result:
                converted.append(result)
                logger.info(f"✅ Office completado en {file_time:.2f}s: {f.name}")
            else:
                logger.error(f"❌ Office falló en {file_time:.2f}s: {f.name}")
        
        office_time = time.perf_counter() - office_start
        logger.info(f"📄 Conversiones Office completadas en {office_time:.2f}s")
    
    total_time = time.perf_counter() - start_time
    logger.info(f"🎯 Total conversiones: {len(converted)}/{len(files)} en {total_time:.2f}s")
    
    return converted, total_time

def optimize_merge_process(pdf_paths: list[Path], out_path: Path) -> float:
    """
    Versión optimizada del proceso de merge con medición de tiempo.
    """
    from main import merge_pdfs, logger
    
    start_time = time.perf_counter()
    
    # Validar archivos antes del merge
    valid_pdfs = []
    for pdf_path in pdf_paths:
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            valid_pdfs.append(pdf_path)
        else:
            logger.warning(f"PDF inválido omitido: {pdf_path}")
    
    if not valid_pdfs:
        raise ValueError("No hay PDFs válidos para unir")
    
    logger.info(f"🔗 Iniciando merge de {len(valid_pdfs)} PDFs...")
    merge_pdfs(valid_pdfs, out_path)
    
    merge_time = time.perf_counter() - start_time
    final_size = out_path.stat().st_size / (1024 * 1024)
    
    logger.info(f"✅ Merge completado en {merge_time:.2f}s | Tamaño final: {final_size:.2f} MB")
    
    return merge_time

def run_optimized_performance_test():
    """
    Ejecuta un test de rendimiento usando las optimizaciones avanzadas.
    """
    from main import list_input_files, TEMP_DIR, OUTPUT_DIR, logger
    import shutil
    
    print("🚀 INICIANDO TEST DE RENDIMIENTO OPTIMIZADO")
    print("=" * 60)
    
    # Preparar ambiente
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    total_start = time.perf_counter()
    
    # Obtener archivos
    files = list_input_files()
    if not files:
        print("❌ No hay archivos en data/input")
        return
    
    print(f"📁 Archivos encontrados: {len(files)}")
    for f in files:
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"   • {f.name} ({f.suffix}) - {size_mb:.2f} MB")
    
    # Conversión optimizada
    print(f"\n⚡ INICIANDO CONVERSIONES OPTIMIZADAS...")
    converted_pdfs, conversion_time = convert_files_with_parallel_optimization(files)
    
    if not converted_pdfs:
        print("❌ No se convirtió ningún archivo")
        return
    
    # Merge optimizado
    print(f"\n🔗 INICIANDO MERGE OPTIMIZADO...")
    test_output = OUTPUT_DIR / "test_optimized_output.pdf"
    merge_time = optimize_merge_process(converted_pdfs, test_output)
    
    # Limpieza
    cleanup_start = time.perf_counter()
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
    if test_output.exists():
        test_output.unlink()
    cleanup_time = time.perf_counter() - cleanup_start
    
    total_time = time.perf_counter() - total_start
    
    # Reporte final
    print(f"\n" + "=" * 60)
    print("📈 RESULTADOS DE OPTIMIZACIÓN")
    print("=" * 60)
    print(f"⏱️  Tiempo de conversiones: {conversion_time:.2f}s")
    print(f"⏱️  Tiempo de merge:       {merge_time:.2f}s")
    print(f"⏱️  Tiempo de limpieza:    {cleanup_time:.3f}s")
    print(f"⏱️  TIEMPO TOTAL:          {total_time:.2f}s")
    print(f"✅ Archivos procesados:    {len(converted_pdfs)}/{len(files)}")
    
    # Comparación con baseline
    baseline_time = 12.80  # Del análisis anterior
    improvement = ((baseline_time - total_time) / baseline_time) * 100
    
    if improvement > 0:
        print(f"🎯 MEJORA: {improvement:.1f}% más rápido que baseline")
    else:
        print(f"📊 Tiempo similar al baseline ({abs(improvement):.1f}% diferencia)")

if __name__ == "__main__":
    run_optimized_performance_test()