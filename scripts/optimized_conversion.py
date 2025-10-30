"""
Versión optimizada de las funciones de conversión con mejoras de rendimiento.
Implementa reutilización de instancias COM, paralelización y optimizaciones específicas.
"""

import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import logging

# Variables globales para reutilizar instancias COM
_word_app = None
_excel_app = None
_word_lock = threading.Lock()
_excel_lock = threading.Lock()

def get_word_instance():
    """Obtiene una instancia reutilizable de Word COM."""
    global _word_app
    try:
        if _word_app is None:
            import win32com.client as win32
            _word_app = win32.DispatchEx("Word.Application")
            _word_app.Visible = False
            # Optimizaciones de rendimiento para Word
            _word_app.Options.DoNotPromptForConvert = True
            _word_app.Options.ConfirmConversions = False
            _word_app.DisplayAlerts = False
        return _word_app
    except Exception as e:
        logging.error(f"Error creando instancia de Word: {e}")
        return None

def get_excel_instance():
    """Obtiene una instancia reutilizable de Excel COM."""
    global _excel_app
    try:
        if _excel_app is None:
            import win32com.client as win32
            _excel_app = win32.DispatchEx("Excel.Application")
            _excel_app.Visible = False
            _excel_app.DisplayAlerts = False
            # Optimizaciones de rendimiento para Excel
            _excel_app.ScreenUpdating = False
            _excel_app.EnableEvents = False
            _excel_app.Calculation = -4135  # xlCalculationManual
        return _excel_app
    except Exception as e:
        logging.error(f"Error creando instancia de Excel: {e}")
        return None

def cleanup_office_instances():
    """Limpia las instancias COM reutilizables."""
    global _word_app, _excel_app
    
    if _word_app:
        try:
            _word_app.Quit()
        except:
            pass
        finally:
            _word_app = None
    
    if _excel_app:
        try:
            _excel_app.Quit()
        except:
            pass
        finally:
            _excel_app = None

def convert_word_to_pdf_optimized(src: Path, dst_pdf: Path):
    """
    Versión optimizada de conversión Word -> PDF usando instancia reutilizable.
    """
    from main import WD_FORMAT_PDF, logger
    
    with _word_lock:  # Sincronización para thread safety
        word = get_word_instance()
        if not word:
            raise RuntimeError("No se pudo obtener instancia de Word")
        
        try:
            logger.info(f"Conversión Word optimizada: {src.name}")
            
            # Rutas absolutas
            src_absolute = src.resolve()
            dst_absolute = dst_pdf.resolve()
            
            # Abrir documento con configuraciones optimizadas
            doc = word.Documents.Open(
                str(src_absolute),
                False,  # ConfirmConversions
                True,   # ReadOnly
                False,  # AddToRecentFiles
                "",     # PasswordDocument
                "",     # PasswordTemplate
                False,  # Revert
                "",     # WritePasswordDocument
                "",     # WritePasswordTemplate
                0       # Format
            )
            
            # Exportar como PDF
            doc.ExportAsFixedFormat(str(dst_absolute), WD_FORMAT_PDF)
            doc.Close(False)
            
            logger.info(f"Word optimizado completado: {dst_pdf.name}")
            
        except Exception as e:
            logger.error(f"Error en conversión Word optimizada {src.name}: {e}")
            raise

def convert_excel_to_pdf_optimized(src: Path, dst_pdf: Path):
    """
    Versión optimizada de conversión Excel -> PDF usando instancia reutilizable.
    """
    from main import XL_TYPE_PDF, logger
    
    with _excel_lock:  # Sincronización para thread safety
        excel = get_excel_instance()
        if not excel:
            raise RuntimeError("No se pudo obtener instancia de Excel")
        
        try:
            logger.info(f"Conversión Excel optimizada: {src.name}")
            
            # Rutas absolutas
            src_absolute = src.resolve()
            dst_absolute = dst_pdf.resolve()
            
            # Abrir libro con configuraciones optimizadas
            wb = excel.Workbooks.Open(
                str(src_absolute),
                False,  # UpdateLinks
                True,   # ReadOnly
                None,   # Format
                "",     # Password
                "",     # WriteResPassword
                True,   # IgnoreReadOnlyRecommended
                None,   # Origin
                None,   # Delimiter
                False,  # Editable
                False,  # Notify
                None,   # Converter
                False   # AddToMru
            )
            
            # Exportar como PDF
            wb.ExportAsFixedFormat(XL_TYPE_PDF, str(dst_absolute))
            wb.Close(False)
            
            logger.info(f"Excel optimizado completado: {dst_pdf.name}")
            
        except Exception as e:
            logger.error(f"Error en conversión Excel optimizada {src.name}: {e}")
            raise

def convert_to_pdf_optimized(src: Path) -> Path | None:
    """
    Versión optimizada de convert_to_pdf que usa instancias reutilizables.
    """
    from main import (
        TEMP_DIR, IMAGE_EXTS, PDF_EXTS, WORD_EXTS, EXCEL_EXTS,
        convert_image_to_pdf, copy_pdf, logger
    )
    
    try:
        dst = TEMP_DIR / (src.stem + ".pdf")
        ext = src.suffix.lower()
        
        logger.info(f"Conversión optimizada: {src.name} ({ext})")
        
        if ext in IMAGE_EXTS:
            convert_image_to_pdf(src, dst)
        elif ext in PDF_EXTS:
            copy_pdf(src, dst)
        elif ext in WORD_EXTS:
            convert_word_to_pdf_optimized(src, dst)
        elif ext in EXCEL_EXTS:
            convert_excel_to_pdf_optimized(src, dst)
        else:
            raise RuntimeError(f"Extensión no soportada: {ext}")
            
        logger.info(f"Conversión optimizada exitosa: {src.name} -> {dst.name}")
        return dst
        
    except Exception as e:
        logger.exception(f"Error en conversión optimizada {src.name}: {e}")
        return None

def convert_files_parallel(files: list[Path], max_workers: int = 2) -> list[Path]:
    """
    Convierte archivos en paralelo para mejorar rendimiento.
    Limita workers para evitar problemas con COM.
    """
    converted = []
    
    # Separar archivos por tipo para optimizar paralelización
    office_files = [f for f in files if f.suffix.lower() in (WORD_EXTS | EXCEL_EXTS)]
    other_files = [f for f in files if f.suffix.lower() in (IMAGE_EXTS | PDF_EXTS)]
    
    # Convertir archivos no-Office en paralelo (más seguro)
    if other_files:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(convert_to_pdf_optimized, f): f 
                for f in other_files
            }
            
            for future in as_completed(future_to_file):
                result = future.result()
                if result:
                    converted.append(result)
    
    # Convertir archivos Office secuencialmente (COM thread-safety)
    for f in office_files:
        result = convert_to_pdf_optimized(f)
        if result:
            converted.append(result)
    
    return converted

# Importaciones necesarias desde main
from main import WORD_EXTS, EXCEL_EXTS, IMAGE_EXTS, PDF_EXTS