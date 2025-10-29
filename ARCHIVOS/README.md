# Directorio de Archivos de Entrada

Este directorio contiene todos los documentos que serán procesados y consolidados en un único PDF.

## Formatos Soportados

- **PDF**: `.pdf` - Se incluyen directamente en el PDF final
- **Word**: `.docx` - Convertidos a PDF automáticamente
- **Excel**: `.xlsx` - Convertidos a PDF automáticamente  
- **Imágenes**: `.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff` - Convertidas a PDF

## Instrucciones

1. Coloque todos los documentos que desea consolidar en este directorio
2. Los archivos serán procesados en orden alfabético
3. Asegúrese de que los archivos no estén corruptos o protegidos
4. Ejecute la aplicación principal para iniciar el proceso de consolidación

## Limitaciones

- Tamaño máximo recomendado por archivo: 100MB
- Los archivos de Word/Excel requieren Microsoft Office instalado
- Los nombres de archivo no deben contener caracteres especiales: `<>:"/\|?*`

## Estructura de Ejemplo

```text
ARCHIVOS/
├── 01_identificacion.pdf
├── 02_certificado_medico.docx
├── 03_factura_hospital.xlsx
└── 04_radiografia.jpg
```

Los archivos serán consolidados en el orden mostrado arriba.