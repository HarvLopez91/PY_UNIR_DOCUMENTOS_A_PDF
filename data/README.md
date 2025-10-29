# Estructura de Datos - PDF Consolidator

## Descripción

Esta carpeta contiene la estructura de datos para el procesamiento de documentos PDF.

## Estructura

### `input/`
Coloque aquí todos los documentos que desea consolidar en un PDF único.

**Formatos soportados:**
- **PDF**: `.pdf` - Se incluyen directamente
- **Word**: `.doc`, `.docx` - Se convierten automáticamente
- **Excel**: `.xlsx` - Se convierten automáticamente  
- **Imágenes**: `.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff` - Se convierten automáticamente

**Importante:**
- Los archivos se procesarán en orden alfabético
- No incluya archivos README.md en esta carpeta (se excluyen automáticamente)
- Asegúrese de que los nombres de archivo no contengan caracteres especiales

### `output/`
Aquí se guardarán los archivos PDF consolidados resultantes.

**Nomenclatura de salida:**
`{identificacion}_{cliente}_{reembolso}.pdf`

**Ejemplo:**
`12345678_EMPRESA_ABC_REF001.pdf`

## Uso

1. Coloque todos sus documentos en `input/`
2. Execute la aplicación (`main.py` o `PDFConsolidator.exe`)
3. Complete los campos solicitados
4. Haga clic en "Consolidar PDF"
5. Encuentre su archivo consolidado en `output/`

## Notas Técnicas

- La aplicación preserva la calidad original de las imágenes
- Los documentos Word y Excel requieren Microsoft Office instalado
- El procesamiento puede tomar tiempo dependiendo del tamaño y cantidad de archivos
- Los archivos temporales se crean en la carpeta `temp/` y se limpian automáticamente
