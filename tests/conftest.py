"""Configuración de pytest para el proyecto PDF Consolidator."""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """Crear directorio temporal para tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_files(temp_dir):
    """Crear archivos de muestra para testing."""
    files = {
        "sample.pdf": b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF",
        "sample.txt": b"Contenido de prueba",
        "sample.jpg": b"\xff\xd8\xff\xe0\x00\x10JFIF"  # Header básico JPEG
    }
    
    created_files = {}
    for filename, content in files.items():
        file_path = temp_dir / filename
        file_path.write_bytes(content)
        created_files[filename] = file_path
    
    return created_files


@pytest.fixture
def mock_office_app(monkeypatch):
    """Mock para aplicaciones de MS Office."""
    class MockWordApp:
        def __init__(self):
            self.visible = False
        
        def quit(self):
            pass
    
    class MockExcelApp:
        def __init__(self):
            self.visible = False
        
        def quit(self):
            pass
    
    def mock_word():
        return MockWordApp()
    
    def mock_excel():
        return MockExcelApp()
    
    monkeypatch.setattr("win32com.client.Dispatch", lambda app: mock_word() if "Word" in app else mock_excel())