# Tests

Este directorio contiene todos los tests unitarios y de integración del proyecto.

## Estructura

```text
tests/
├── __init__.py
├── conftest.py              # Configuración de pytest
├── test_conversion.py       # Tests de conversión de archivos
├── test_pdf_merge.py        # Tests de unión de PDFs
├── test_gui.py              # Tests de interfaz gráfica
├── test_utils.py            # Tests de utilidades
└── fixtures/                # Archivos de prueba
    ├── sample.pdf
    ├── sample.docx
    ├── sample.xlsx
    └── sample.jpg
```

## Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=src

# Tests específicos
pytest tests/test_conversion.py

# Tests con output detallado
pytest -v
```

## Escribir Tests

Los tests deben seguir las convenciones de naming:

- Archivos: `test_*.py`
- Funciones: `test_*`
- Clases: `Test*`

### Ejemplo de test

```python
def test_pdf_conversion():
    """Test que verifica la conversión básica de PDF."""
    # Arrange
    input_file = Path("sample.pdf")
    
    # Act
    result = convert_to_pdf(input_file)
    
    # Assert
    assert result.exists()
    assert result.suffix == ".pdf"
```