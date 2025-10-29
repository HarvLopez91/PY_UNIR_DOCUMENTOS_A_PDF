# Directorio Temporal (Temp)

Este directorio se utiliza para almacenar archivos temporales durante el proceso de conversión de documentos a PDF.

## Propósito

- **Conversión de Office**: Almacena PDFs temporales generados desde Word/Excel
- **Procesamiento de imágenes**: Archivos intermedios durante la conversión de imágenes
- **Archivos de trabajo**: Documentos temporales necesarios para el proceso de merge

## Comportamiento

### Creación Automática
- Los archivos temporales se crean automáticamente durante la conversión
- Cada proceso genera archivos únicos para evitar conflictos

### Limpieza Automática
- Los archivos se eliminan automáticamente al completar la consolidación
- En caso de error, algunos archivos temporales pueden permanecer

### Estructura Típica Durante Procesamiento
```text
TEMP_CONVERSION/
├── temp_word_conversion_001.pdf
├── temp_excel_conversion_002.pdf
├── temp_image_conversion_003.pdf
└── working_merge_file.pdf
```

## Mantenimiento

- **Limpieza manual**: Puede eliminar archivos manualmente si es necesario
- **Espacio en disco**: Monitoree el espacio disponible durante conversiones grandes
- **Permisos**: Asegúrese de que la aplicación tenga permisos de escritura

## Solución de Problemas

Si encuentra archivos temporales persistentes:

1. Cierre completamente la aplicación
2. Elimine manualmente los archivos en este directorio
3. Reinicie la aplicación y reintente el proceso

⚠️ **Advertencia**: No modifique archivos en este directorio mientras la aplicación esté ejecutándose.