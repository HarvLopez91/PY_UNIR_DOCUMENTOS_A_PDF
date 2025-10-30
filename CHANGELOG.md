# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere al [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2025-10-30

### Fixed

- **Optimización crítica de rendimiento**: Implementación de reutilización de instancias COM para conversión de documentos Word/Excel
  - Archivos .doc ahora se convierten ~59-82% más rápido
  - Tiempo total del proceso reducido de ~12.8s a ~4.2s (67% mejora)
  - Configuraciones optimizadas: deshabilita alertas, actualizaciones de pantalla, conversiones automáticas
- **Sistema de versionado centralizado**: Implementación de archivo `VERSION` como fuente única de verdad
  - Elimina duplicación de versiones en código
  - Sincronización automática entre UI y documentación
- **Limpieza mejorada de recursos**: Instancias COM se limpian al finalizar proceso completo (no por archivo)
- **Feedback visual mejorado**: Progreso en tiempo real durante conversiones

### Changed

- `APP_VERSION` ahora lee dinámicamente desde archivo `VERSION`
- README.md sincronizado con versión actual
- Implementación de locks thread-safe para operaciones COM

### Technical

- Migración de instancias COM por archivo a instancias reutilizables globales
- Parámetros optimizados para apertura de documentos Office (ReadOnly, sin conversiones)
- Sistema de logging mejorado para monitoreo de rendimiento

## [1.2.0] - 2025-10-29

### Added

- Sistema de logging con rotación automática
- Validación de archivos de entrada
- Soporte para múltiples formatos de imagen (TIF, TIFF)
- Interfaz gráfica mejorada con feedback visual
- Sanitización automática de nombres de archivo
- Configuración de proyecto con pyproject.toml

### Changed

- Migración a pathlib para manejo de rutas
- Mejora en el manejo de errores
- Optimización del proceso de conversión
- Reorganización de la estructura del proyecto

### Fixed

- Problemas con caracteres especiales en nombres de archivo
- Memory leaks en conversiones de archivos grandes
- Errores de compatibilidad con diferentes versiones de Office

### Security

- Validación de tipos de archivo antes del procesamiento
- Sanitización de nombres de archivo para prevenir ataques de path traversal

## [1.1.0] - 2025-09-15

### Added (v1.1.0)

- Soporte para archivos Excel (.xlsx)
- Conversión automática de documentos Word (.docx)
- Sistema de directorios temporales
- Validación de extensiones de archivo

### Changed (v1.1.0)

- Mejora en la interfaz de usuario
- Optimización del proceso de merge de PDFs

### Fixed (v1.1.0)

- Errores en la conversión de imágenes grandes
- Problemas de codificación en nombres de archivo

## [1.0.0] - 2025-08-01

### Added (v1.0.0)

- Funcionalidad básica de consolidación de PDFs
- Interfaz gráfica con Tkinter
- Soporte para imágenes JPG y PNG
- Sistema básico de logging
- Conversión de imágenes a PDF

### Technical

- Implementación inicial con pypdf
- Integración con img2pdf para conversión de imágenes
- Estructura básica de directorios

## [Unreleased]

### Planned

- Soporte para PowerPoint (.pptx)
- Configuración de calidad de compresión
- Modo batch para procesamiento automático
- Soporte para múltiples idiomas
- Plugin system para nuevos formatos
- API REST para integración externa

---

## Tipos de cambios

- `Added` para nuevas funcionalidades
- `Changed` para cambios en funcionalidades existentes
- `Deprecated` para funcionalidades que serán removidas pronto
- `Removed` para funcionalidades removidas
- `Fixed` para corrección de bugs
- `Security` para mejoras de seguridad
- `Technical` para cambios técnicos internos