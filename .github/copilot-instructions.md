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

### Política de Reutilización de Archivos
- **OBLIGATORIO**: Antes de crear nuevos archivos, verificar si ya existe uno que cumpla el mismo objetivo
- **Verificación completa**: Buscar en todo el proyecto (archivos .py, .bat, .sh, .md, .txt, etc.)
- **Reutilización primera**: Si existe un archivo similar, reutilizarlo o ampliarlo en lugar de duplicarlo
- **Nomenclatura coherente**: Mantener consistencia en nombres de archivos relacionados
- **Documentación**: Si se modifica un archivo existente, actualizar su documentación interna
- **Evitar redundancia**: No crear archivos que implementen la misma funcionalidad

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
- **Office**: `.doc`, `.docx`, `.xlsx` - Conversión via COM automation (Windows)
- **Imágenes**: `.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff` - Conversión con img2pdf

### Salida
- **PDF consolidado**: Nombre formato `{identificacion}_{cliente}_{reembolso}.pdf`

## Ejecución y Distribución

### Modo Desarrollador
1. **Activar entorno virtual**: `venv\Scripts\activate`
2. **Ejecutar aplicación**: `python main.py`
3. **Desarrollo con hot-reload**: Modificar código y re-ejecutar
4. **Debugging**: Usar logs en directorio `logs/` para troubleshooting

### Modo Usuario (Distribución)
1. **Generar ejecutable**: Usar `scripts\build_exe.bat` tras cada cambio
2. **Carpeta dist**: Contiene la distribución completa para usuarios finales
3. **Estructura dist**: `PDFConsolidator.exe` + carpetas `data/`, `temp/`, `logs/`
4. **Entrega**: Comprimir carpeta `dist/` completa y entregar al usuario
5. **Instalación**: Usuario descomprime y ejecuta `PDFConsolidator.exe`

### Política de Distribución
- **OBLIGATORIO**: Generar nuevo `.exe` tras cada modificación de código
- **Carpeta dist**: Es la versión completa para usuarios finales (no desarrolladores)
- **Testing**: Probar el `.exe` generado antes de distribución
- **Versionado**: Actualizar `APP_VERSION` en `main.py` con cada release
- **Documentación**: README.md específico incluido en `dist/` para usuarios

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

### Política de Pruebas Pre-Commit
- **OBLIGATORIO**: Realizar pruebas de la aplicación antes de cualquier commit
- **Verificación funcional**: Probar que la aplicación ejecuta correctamente
- **Validación de cambios**: Verificar que las modificaciones funcionan como se espera
- **Pruebas de regresión**: Confirmar que no se rompió funcionalidad existente
- **Testing en directorio tests/**: Ejecutar pruebas formales cuando sea aplicable
- **Documentar resultados**: Incluir en el mensaje de commit si las pruebas fueron exitosas

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

## Política de Versionado (OBLIGATORIA)

### Fuente Única de la Versión
- **ARCHIVO VERSION**: La versión del proyecto se define SOLO en el archivo raíz `VERSION` (ej.: `1.2.1`)
- **CONSUMO OBLIGATORIO**: La UI, README, CHANGELOG y scripts de build **deben leer** desde `VERSION`
- **PROHIBICIÓN**: Está prohibido "hardcodear" la versión en múltiples archivos

### SemVer en Desarrollo
- **MAJOR**: Cambios incompatibles que rompen la API existente
- **MINOR**: Nuevas funciones compatibles con versiones anteriores
- **PATCH**: Correcciones (bugfix), documentación menor o ajustes no funcionales

### Cuándo Incrementar Versión
- **PATCH**: Si se corrige un bug, mejora de rendimiento, optimización
- **MINOR**: Si se añade funcionalidad sin romper compatibilidad
- **MAJOR**: Si hay cambios incompatibles con versiones anteriores

### Archivos que Deben Sincronizarse SIEMPRE
- `VERSION` → fuente de verdad única
- Banner/Acerca de la app (UI) → debe leer desde `VERSION`
- `README.md` (sección "Versión actual") → debe referenciar `VERSION`
- `CHANGELOG.md` (entrada con fecha y resumen) → debe documentar cambios
- Metadatos de empaquetado/build si aplican

### Checklist Previo a Commit de Versión
1. **Verificar centralización**: Confirmar que **todos** los lugares consumen `VERSION` (sin duplicados)
2. **Actualizar CHANGELOG.md** con:
   - Versión, fecha, categoría (feat/fix/refactor/docs/perf)
   - Bullets claros de qué cambió, por qué y cómo impacta
   - Sección Technical para cambios internos
3. **Confirmar UI**: Verificar que la interfaz muestra la versión correcta
4. **Ejecutar pruebas**: Realizar tests básicos y verificación de arranque
5. **Validar build**: Confirmar que el ejecutable se genera correctamente

### Formato de Commit y Tagging
- **Mensaje de commit** (formato estricto):
  ```
  chore(release): vX.Y.Z
  
  - Sincroniza UI, README y CHANGELOG con VERSION
  - [Resumen breve de cambios principales]
  - [Categoría: feat/fix/perf/refactor/docs]
  ```
- **Tras aprobación**: Crear tag anotado `vX.Y.Z` y push de tags

### Acción de Copilot (OBLIGATORIA)
- **Detección previa**: Antes de proponer un bump, detectar **desalineaciones** entre `VERSION`, UI y docs
- **Presentar diff**: Mostrar diferencias encontradas para corrección
- **No destructivo**: No ejecutar cambios sin confirmación del usuario
- **Sugerencia inteligente**: 
  - Para bugfix (ej. corrección de `.doc`) → **sugerir PATCH** (ej.: `1.2.0 → 1.2.1`)
  - Para nueva función → **sugerir MINOR** (ej.: `1.2.1 → 1.3.0`)
  - Para breaking changes → **sugerir MAJOR** (ej.: `1.3.0 → 2.0.0`)

### Criterios de Aceptación
- **Origen único**: Un solo archivo `VERSION` y **0 strings duplicados** de versión en código
- **Sincronización perfecta**: README y UI muestran exactamente la misma versión
- **Documentación completa**: `CHANGELOG.md` actualizado y coherente con el commit
- **Tag válido**: Tag `vX.Y.Z` existente y sincronizado con `VERSION`
- **Build funcional**: Ejecutable generado correctamente con nueva versión