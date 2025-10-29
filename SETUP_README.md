# Guía de Configuración - PDF Consolidator

## 🚀 Configuración Rápida

### Prerrequisitos
- **Python 3.8+** instalado en el sistema
- **Windows** con MS Office (para conversión de documentos .doc/.docx/.xlsx)
- Permisos de escritura en el directorio del proyecto

### 📦 Instalación Automática

1. **Clonar o descargar** el proyecto en tu directorio de trabajo
2. **Ejecutar script de configuración:**
   ```bash
   cd PY_UNIR_DOCUMENTOS_A_PDF
   scripts\setup.bat
   ```

El script automáticamente:
- ✅ Verifica que Python esté instalado
- ✅ Crea un entorno virtual limpio
- ✅ Instala todas las dependencias necesarias
- ✅ Configura la estructura de directorios
- ✅ Verifica que la aplicación funcione correctamente

### 🎯 Uso de la Aplicación

Después de la configuración exitosa:

```bash
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar aplicación
python main.py
```

### 🏗️ Generar Ejecutable

Para crear un ejecutable independiente:

```bash
# Desde el directorio raíz del proyecto
scripts\build_exe.bat
```

El ejecutable se generará en la carpeta `dist/` con todos los assets incluidos.

### 📂 Estructura del Proyecto

```
PY_UNIR_DOCUMENTOS_A_PDF/
├── main.py                    # Aplicación principal
├── requirements.txt           # Dependencias de producción
├── requirements-dev.txt       # Herramientas de desarrollo
├── scripts/
│   ├── setup.bat             # Script de configuración
│   └── build_exe.bat         # Generador de ejecutable
├── assets/
│   └── Expansión.png         # Logo de la empresa
├── data/
│   ├── input/                # Documentos de entrada
│   └── output/               # PDFs consolidados
├── venv/                     # Entorno virtual (generado)
├── dist/                     # Ejecutable para distribución
└── logs/                     # Archivos de log
```

### 🔧 Solución de Problemas

#### Error: "Python no está instalado"
- Instalar Python desde [python.org](https://python.org)
- Verificar que Python esté en el PATH del sistema

#### Error: "No se encuentra main.py"
- Ejecutar el script desde el directorio raíz del proyecto
- Verificar que el archivo `main.py` exista

#### Error en instalación de dependencias
- Verificar conexión a internet
- Ejecutar como administrador si es necesario
- Verificar que no haya restricciones de firewall/proxy

#### Problema con MS Office
- Verificar que MS Office esté instalado
- Ejecutar la aplicación como administrador para conversiones COM

### 🛠️ Desarrollo

Para contribuir al desarrollo:

```bash
# Configurar entorno de desarrollo
scripts\setup.bat
# Responder "Y" cuando pregunte por dependencias de desarrollo

# Activar entorno
venv\Scripts\activate

# Herramientas disponibles
black .                # Formatear código
flake8 .               # Verificar estilo
mypy .                 # Verificación de tipos
pytest                 # Ejecutar tests
```

### 📋 Dependencias Principales

**Producción:**
- `img2pdf` - Conversión de imágenes a PDF
- `pypdf` - Manipulación de archivos PDF
- `pyinstaller` - Generación de ejecutables
- `pywin32` - Integración con MS Office (Windows)

**Desarrollo:**
- `black` - Formateo de código
- `flake8` - Análisis estático
- `mypy` - Verificación de tipos
- `pytest` - Framework de testing
- `pre-commit` - Hooks de validación

### 📞 Soporte

Si encuentras problemas:
1. Verificar que todas las dependencias estén instaladas
2. Comprobar los logs en la carpeta `logs/`
3. Ejecutar `python main.py` desde la línea de comandos para ver errores detallados
4. Revisar que los archivos de entrada estén en formato soportado

---
**Nota:** Este proyecto está optimizado para entornos Windows con MS Office instalado.