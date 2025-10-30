"""
Script para analizar el rendimiento del proceso de conversión y consolidación.
Mide tiempos de cada fase para identificar cuellos de botella.
"""

import time
import statistics
from pathlib import Path
import sys
import os

# Agregar el directorio padre al path para importar main
sys.path.append(str(Path(__file__).parent.parent))

from main import (
    convert_to_pdf, merge_pdfs, list_input_files, 
    INPUT_DIR, OUTPUT_DIR, TEMP_DIR, logger,
    IMAGE_EXTS, WORD_EXTS, EXCEL_EXTS, PDF_EXTS
)
import shutil

class PerformanceAnalyzer:
    def __init__(self):
        self.results = {
            'file_analysis': [],
            'conversions': [],
            'merge_time': 0,
            'total_time': 0,
            'cleanup_time': 0
        }
    
    def analyze_file(self, file_path: Path) -> dict:
        """Analiza un archivo individual y retorna métricas."""
        start_time = time.perf_counter()
        
        # Obtener información básica del archivo
        size_mb = file_path.stat().st_size / (1024 * 1024)
        ext = file_path.suffix.lower()
        
        # Categorizar tipo de archivo
        if ext in IMAGE_EXTS:
            file_type = "Imagen"
        elif ext in WORD_EXTS:
            file_type = "Word"
        elif ext in EXCEL_EXTS:
            file_type = "Excel"
        elif ext in PDF_EXTS:
            file_type = "PDF"
        else:
            file_type = "Desconocido"
        
        analysis_time = time.perf_counter() - start_time
        
        return {
            'name': file_path.name,
            'type': file_type,
            'size_mb': round(size_mb, 2),
            'extension': ext,
            'analysis_time': analysis_time
        }
    
    def measure_conversion(self, file_path: Path) -> dict:
        """Mide el tiempo de conversión de un archivo específico."""
        start_time = time.perf_counter()
        
        # Realizar conversión
        result_pdf = convert_to_pdf(file_path)
        
        conversion_time = time.perf_counter() - start_time
        
        # Obtener tamaño del PDF resultante si existe
        output_size_mb = 0
        if result_pdf and result_pdf.exists():
            output_size_mb = result_pdf.stat().st_size / (1024 * 1024)
        
        return {
            'input_file': file_path.name,
            'success': result_pdf is not None,
            'conversion_time': conversion_time,
            'output_size_mb': round(output_size_mb, 2) if result_pdf else 0,
            'output_path': result_pdf
        }
    
    def run_performance_test(self):
        """Ejecuta análisis completo de rendimiento."""
        print("🔍 Iniciando análisis de rendimiento...")
        print("=" * 60)
        
        # Preparar directorios
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR, ignore_errors=True)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        
        total_start = time.perf_counter()
        
        # 1. Análisis de archivos de entrada
        print("\n📁 FASE 1: Análisis de archivos de entrada")
        print("-" * 40)
        
        files = list_input_files()
        if not files:
            print("❌ No hay archivos en data/input")
            return
        
        for file_path in files:
            file_info = self.analyze_file(file_path)
            self.results['file_analysis'].append(file_info)
            print(f"📄 {file_info['name']:30} | {file_info['type']:8} | {file_info['size_mb']:6.2f} MB")
        
        total_input_size = sum(f['size_mb'] for f in self.results['file_analysis'])
        print(f"\n📊 Total archivos: {len(files)} | Tamaño total: {total_input_size:.2f} MB")
        
        # 2. Conversiones individuales
        print("\n🔄 FASE 2: Conversiones individuales")
        print("-" * 40)
        
        converted_pdfs = []
        
        for file_path in files:
            print(f"⚡ Convirtiendo: {file_path.name}...", end=" ")
            
            conversion_result = self.measure_conversion(file_path)
            self.results['conversions'].append(conversion_result)
            
            if conversion_result['success']:
                converted_pdfs.append(conversion_result['output_path'])
                print(f"✅ {conversion_result['conversion_time']:.2f}s | {conversion_result['output_size_mb']:.2f} MB")
            else:
                print(f"❌ FALLO en {conversion_result['conversion_time']:.2f}s")
        
        # 3. Proceso de merge
        print("\n🔗 FASE 3: Unión de PDFs")
        print("-" * 40)
        
        if converted_pdfs:
            merge_start = time.perf_counter()
            
            test_output = OUTPUT_DIR / "test_performance_output.pdf"
            try:
                merge_pdfs(converted_pdfs, test_output)
                self.results['merge_time'] = time.perf_counter() - merge_start
                
                final_size = test_output.stat().st_size / (1024 * 1024)
                print(f"✅ Merge completado en {self.results['merge_time']:.2f}s | PDF final: {final_size:.2f} MB")
                
                # Limpiar archivo de prueba
                if test_output.exists():
                    test_output.unlink()
                    
            except Exception as e:
                print(f"❌ Error en merge: {e}")
                self.results['merge_time'] = time.perf_counter() - merge_start
        
        # 4. Limpieza
        print("\n🧹 FASE 4: Limpieza de archivos temporales")
        print("-" * 40)
        
        cleanup_start = time.perf_counter()
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR, ignore_errors=True)
        self.results['cleanup_time'] = time.perf_counter() - cleanup_start
        print(f"✅ Limpieza completada en {self.results['cleanup_time']:.3f}s")
        
        # Tiempo total
        self.results['total_time'] = time.perf_counter() - total_start
        
        # 5. Reporte final
        self.generate_report()
    
    def generate_report(self):
        """Genera reporte detallado de rendimiento."""
        print("\n" + "="*60)
        print("📈 REPORTE DE RENDIMIENTO")
        print("="*60)
        
        # Resumen de tiempos
        conversion_times = [c['conversion_time'] for c in self.results['conversions'] if c['success']]
        
        print(f"\n⏱️  TIEMPOS GENERALES:")
        print(f"   • Tiempo total del proceso: {self.results['total_time']:.2f}s")
        print(f"   • Tiempo de conversiones:   {sum(conversion_times):.2f}s")
        print(f"   • Tiempo de merge:          {self.results['merge_time']:.2f}s")
        print(f"   • Tiempo de limpieza:       {self.results['cleanup_time']:.3f}s")
        
        if conversion_times:
            print(f"\n📊 ESTADÍSTICAS DE CONVERSIÓN:")
            print(f"   • Conversión más rápida:    {min(conversion_times):.2f}s")
            print(f"   • Conversión más lenta:     {max(conversion_times):.2f}s")
            print(f"   • Tiempo promedio:          {statistics.mean(conversion_times):.2f}s")
            print(f"   • Mediana:                  {statistics.median(conversion_times):.2f}s")
        
        # Análisis por tipo de archivo
        print(f"\n🗂️  RENDIMIENTO POR TIPO DE ARCHIVO:")
        type_performance = {}
        
        for i, conv in enumerate(self.results['conversions']):
            if conv['success']:
                file_info = self.results['file_analysis'][i]
                file_type = file_info['type']
                
                if file_type not in type_performance:
                    type_performance[file_type] = []
                
                type_performance[file_type].append({
                    'time': conv['conversion_time'],
                    'size_mb': file_info['size_mb'],
                    'rate_mb_per_s': file_info['size_mb'] / conv['conversion_time'] if conv['conversion_time'] > 0 else 0
                })
        
        for file_type, data in type_performance.items():
            avg_time = statistics.mean([d['time'] for d in data])
            avg_rate = statistics.mean([d['rate_mb_per_s'] for d in data])
            count = len(data)
            
            print(f"   • {file_type:8}: {count:2} archivos | Promedio: {avg_time:5.2f}s | Velocidad: {avg_rate:5.2f} MB/s")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        
        # Detectar cuellos de botella
        if self.results['merge_time'] > sum(conversion_times) * 0.3:
            print("   ⚠️  El proceso de merge consume tiempo significativo")
            print("      → Considerar optimización del merge de PDFs")
        
        slowest_conversions = sorted(
            [(conv, self.results['file_analysis'][i]) for i, conv in enumerate(self.results['conversions']) if conv['success']], 
            key=lambda x: x[0]['conversion_time'], 
            reverse=True
        )[:3]
        
        if slowest_conversions:
            print("   🐌 Archivos más lentos de convertir:")
            for conv, file_info in slowest_conversions:
                print(f"      → {file_info['name']:25} ({file_info['type']}) - {conv['conversion_time']:.2f}s")
        
        # Archivos fallidos
        failed_conversions = [conv for conv in self.results['conversions'] if not conv['success']]
        if failed_conversions:
            print("   ❌ Archivos que fallaron en conversión:")
            for conv in failed_conversions:
                print(f"      → {conv['input_file']}")

if __name__ == "__main__":
    analyzer = PerformanceAnalyzer()
    analyzer.run_performance_test()