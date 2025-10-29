# Instrucciones para GitHub Copilot

## Descripción del Proyecto

Este es un proyecto Python para consolidar múltiples documentos en un archivo PDF único. La aplicación tiene una interfaz gráfica desarrollada con Tkinter y permite convertir y unir documentos de diferentes formatos (PDF, DOCX, XLSX, imágenes JPG/PNG/TIF) en un solo archivo PDF organizado.

## Arquitectura y Estructura

```
PY_UNIR_DOCUMENTOS_A_PDF/
├── main.py                 # Aplicación principal con GUI Tkinter
├── ARCHIVOS/              # Directorio de entrada para documentos
├── CONSOLIDADOS/          # Directorio de salida para PDFs consolidados
├── TEMP_CONVERSION/       # Directorio temporal para conversiones
├── assets/                # Recursos gráficos (logos, imágenes)
├── logs/                  # Archivos de log de la aplicación
└── test_data/             # Datos de prueba
```

## Estándares de Codificación

### Convenciones de Nomenclatura
- **Variables y funciones**: snake_case (ejemplo: `final_pdf_name`, `input_dir`)
- **Constantes**: UPPER_SNAKE_CASE (ejemplo: `APP_VERSION`, `ALLOWED_EXTS`)
- **Clases**: PascalCase (si se agregan en el futuro)
- **Archivos**: snake_case.py

### Estilo de Código
- Seguir PEP 8 para el formato de código Python
- Límite de línea: 88 caracteres (compatible con Black formatter)
- Usar type hints para todas las funciones nuevas
- Documentar funciones con docstrings en formato Google/NumPy

### Estructura de Funciones
```python
def function_name(param1: str, param2: int) -> bool:
    """Descripción breve de la función.
    
    Args:
        param1: Descripción del parámetro 1
        param2: Descripción del parámetro 2
        
    Returns:
        Descripción del valor de retorno
        
    Raises:
        Exception: Descripción de cuándo se lanza
    """
    # Implementación
    pass
```

## Tecnologías y Dependencias

### Core Dependencies
- **Python 3.8+**: Versión mínima requerida
- **tkinter**: GUI nativa de Python (incluida por defecto)
- **pathlib**: Manejo moderno de rutas de archivos

### Conversion Libraries
- **img2pdf**: Conversión de imágenes a PDF
- **pypdf**: Manipulación y merge de archivos PDF
- **pywin32**: Integración con MS Office (Windows only)

### Utilities
- **logging**: Sistema de logs con rotación
- **unicodedata**: Normalización de caracteres para nombres de archivo

## Patterns y Mejores Prácticas

### Manejo de Errores
- Usar try-catch específicos para cada tipo de operación
- Registrar errores en el sistema de logging
- Mostrar mensajes de error amigables al usuario en la GUI
- No silenciar excepciones sin logging

### Logging
- Usar el logger configurado: `logger.info()`, `logger.error()`, etc.
- Incluir contexto relevante en los mensajes de log
- Configurar rotación de logs para evitar archivos grandes

### Gestión de Archivos
- Usar `pathlib.Path` para todas las operaciones de archivo
- Crear directorios con `mkdir(parents=True, exist_ok=True)`
- Limpiar archivos temporales después del uso
- Validar extensiones de archivo antes del procesamiento

### GUI con Tkinter
- Separar lógica de negocio de la presentación
- Usar StringVar para variables de control
- Implementar validación de entrada en tiempo real
- Proporcionar feedback visual al usuario durante operaciones largas

## Reglas de Desarrollo

### Al Agregar Nuevas Funcionalidades
1. **Mantener compatibilidad**: Asegurar que funcione en Windows con MS Office
2. **Validar entradas**: Verificar tipos de archivo y contenido antes del procesamiento
3. **Manejo de memoria**: Liberar recursos después de conversiones grandes
4. **Testing**: Agregar casos de prueba en el directorio `test_data/`

### Al Modificar Código Existente
1. **Preservar funcionalidad**: No romper conversiones existentes
2. **Mantener interfaz**: Cambios en GUI deben ser intuitivos
3. **Actualizar logging**: Agregar logs apropiados para nuevas funciones
4. **Documentar cambios**: Actualizar comentarios y docstrings

### Seguridad y Robustez
- Sanitizar nombres de archivo para evitar problemas del sistema de archivos
- Validar archivos de entrada antes del procesamiento
- Manejar archivos corruptos o inválidos graciosamente
- Limitar el tamaño de archivos procesados para evitar problemas de memoria

## Formato de Archivos Soportados

### Entrada
- **PDF**: `.pdf` - Procesamiento directo con pypdf
- **Office**: `.docx`, `.xlsx` - Conversión via COM automation (Windows)
- **Imágenes**: `.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff` - Conversión con img2pdf

### Salida
- **PDF consolidado**: Nombre formato `{identificacion}_{cliente}_{reembolso}.pdf`

## Convenciones de Commit

### Formato de Mensajes de Commit
- **Idioma**: Preferiblemente en español
- **Formato**: Usar viñetas para describir cambios múltiples
- **Estructura**: `tipo: descripción breve` seguido de lista con viñetas

### Tipos de Commit
- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bugs
- `refactor:` - Refactoring sin cambio de funcionalidad
- `docs:` - Cambios en documentación
- `style:` - Cambios de formato/estilo
- `test:` - Adición o modificación de tests
- `chore:` - Tareas de mantenimiento

### Ejemplo de Commit Mensaje
```
feat: Agregar funcionalidad de conversión de PowerPoint

- Soporte para archivos .pptx
- Integración con COM automation de PowerPoint
- Validación de archivos de entrada
- Manejo de errores específicos para PowerPoint
- Tests unitarios para nueva funcionalidad
```

### Buenas Prácticas
- Usar presente indicativo: "Agregar" en lugar de "Agregado"
- Ser específico sobre los cambios realizados
- Incluir contexto relevante cuando sea necesario
- Limitar la primera línea a 50 caracteres cuando sea posible
- Usar viñetas para enumerar cambios específicos

## Consideraciones Especiales

### Compatibilidad Windows/Office
- El código asume entorno Windows con MS Office instalado
- Usar `HAS_WIN32` flag para verificar disponibilidad de pywin32
- Proporcionar mensajes de error claros si faltan dependencias

### Procesamiento de Archivos
- Mantener orden alfabético de archivos en el PDF final
- Preservar calidad de imágenes durante conversión
- Optimizar PDFs resultantes para tamaño cuando sea posible

### Interfaz de Usuario
- Proporcionar feedback visual durante operaciones de conversión
- Validar campos de entrada antes de procesar
- Mostrar progreso para operaciones que toman tiempo
- Permitir cancelación de operaciones largas

## Políticas de Testing y Pruebas

### Ejecución de Tests
- **Ubicación exclusiva**: Ejecutar todos los tests únicamente en la carpeta `tests/` del repositorio
- **Aislamiento**: No crear archivos de prueba fuera del directorio `tests/`
- **Organización**: Mantener estructura clara dentro de `tests/` para diferentes tipos de pruebas

### Limpieza Post-Pruebas
- **Archivos generados**: Eliminar automáticamente todos los archivos generados durante las pruebas
- **Archivos temporales**: Limpiar completamente cualquier archivo temporal creado
- **Estado limpio**: Dejar el directorio `tests/` en estado original tras la ejecución

### Archivos de Documentación de Pruebas
- **Archivos .md**: Si se crean archivos Markdown para revisión, **consultar antes de eliminarlos**
- **Reportes de prueba**: Preguntar al usuario si desea conservar reportes o documentación generada
- **Logs de testing**: Mantener logs solo si se solicita explícitamente

### Mejores Prácticas
- Usar fixtures y datos de prueba contenidos en `tests/fixtures/`
- Crear tests independientes que no dependan de estado externo
- Validar limpieza automática al final de cada suite de pruebas
- Proporcionar resumen de resultados antes de la limpieza