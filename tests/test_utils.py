"""Tests unitarios básicos para utilidades del proyecto."""

import pytest
from pathlib import Path
import sys
import os

# Agregar src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Importar funciones del main.py (temporalmente)
sys.path.insert(0, str(Path(__file__).parent.parent))
from main import sanitize_component, final_pdf_name


class TestUtilities:
    """Tests para funciones de utilidad."""
    
    def test_sanitize_component_basic(self):
        """Test sanitización básica de componentes."""
        result = sanitize_component("nombre_normal")
        assert result == "nombre_normal"
    
    def test_sanitize_component_special_chars(self):
        """Test sanitización con caracteres especiales."""
        result = sanitize_component("nombre<>con:caracteres/especiales")
        assert result == "nombre__con_caracteres_especiales"
    
    def test_sanitize_component_spaces(self):
        """Test sanitización con espacios múltiples."""
        result = sanitize_component("nombre   con    espacios")
        assert result == "nombre con espacios"
    
    def test_sanitize_component_accents(self):
        """Test sanitización con acentos."""
        result = sanitize_component("José María")
        assert result == "Jose Maria"
    
    def test_final_pdf_name_basic(self):
        """Test generación de nombre de PDF básico."""
        result = final_pdf_name("12345", "Juan Perez", "67890")
        assert result == "12345_Juan_Perez_67890.pdf"
    
    def test_final_pdf_name_special_chars(self):
        """Test generación de nombre con caracteres especiales."""
        result = final_pdf_name("123/45", "José María", "678<90")
        assert result == "123_45_Jose_Maria_678_90.pdf"
    
    def test_final_pdf_name_empty_fields(self):
        """Test generación de nombre con campos vacíos."""
        result = final_pdf_name("", "Cliente", "")
        assert result == "Cliente.pdf"
    
    def test_final_pdf_name_spaces(self):
        """Test generación de nombre con espacios."""
        result = final_pdf_name("  123  ", "  Juan Perez  ", "  456  ")
        assert result == "123_Juan_Perez_456.pdf"


class TestFileOperations:
    """Tests para operaciones de archivo."""
    
    def test_file_validation(self, sample_files):
        """Test validación de archivos."""
        pdf_file = sample_files["sample.pdf"]
        assert pdf_file.exists()
        assert pdf_file.suffix == ".pdf"
    
    def test_directory_creation(self, temp_dir):
        """Test creación de directorios."""
        new_dir = temp_dir / "test_subdir" / "nested"
        new_dir.mkdir(parents=True, exist_ok=True)
        assert new_dir.exists()
        assert new_dir.is_dir()


if __name__ == "__main__":
    pytest.main([__file__])