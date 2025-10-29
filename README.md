# PDF Consolidator

Aplicación de escritorio para consolidar múltiples documentos de diferentes formatos en un único archivo PDF organizado.

## 🚀 Características

- **Múltiples formatos soportados**: PDF, DOCX, XLSX, JPG, PNG, TIF
- **Interfaz gráfica intuitiva**: Desarrollada con Tkinter
- **Conversión automática**: Convierte documentos de Office e imágenes a PDF
- **Organización automática**: Ordena los archivos alfabéticamente en el PDF final
- **Nomenclatura inteligente**: Genera nombres de archivo basados en identificación, cliente y reembolso
- **Logging completo**: Sistema de logs con rotación automática

## 📋 Requisitos

- **Sistema Operativo**: Windows 10/11
- **Python**: 3.8 o superior
- **Microsoft Office**: Word y Excel (para conversión de documentos .docx/.xlsx)

## 🛠️ Instalación

### Opción 1: Configuración automática (Recomendada)

```bash
# Ejecutar script de configuración automática
scripts\setup.bat
```

### Opción 2: Instalación manual

```bash
# Clonar el repositorio
git clone https://github.com/HarvLopez91/PY_UNIR_DOCUMENTOS_A_PDF.git
cd PY_UNIR_DOCUMENTOS_A_PDF

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Opción 3: Instalación en modo desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Instalar en modo editable
pip install -e .

# Configurar pre-commit hooks
pre-commit install
```
```

## 🎯 Uso

### Ejecución de la aplicación

```bash
python main.py
```

### Flujo de trabajo

1. **Preparar documentos**: Coloque todos los documentos en la carpeta `ARCHIVOS/`
2. **Ejecutar aplicación**: Inicie `main.py`
3. **Completar formulario**:
   - Identificación del cliente
   - Nombre del cliente
   - Número de reembolso
4. **Procesar**: Haga clic en "Consolidar PDFs"
5. **Resultado**: El PDF consolidado se guardará en `CONSOLIDADOS/`

### Formatos soportados

| Formato | Extensión | Método de conversión |
|---------|-----------|---------------------|
| PDF | `.pdf` | Procesamiento directo |
| Word | `.docx` | COM Automation (MS Word) |
| Excel | `.xlsx` | COM Automation (MS Excel) |
| Imágenes | `.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff` | img2pdf |

## 📁 Estructura del Proyecto

```text
PY_UNIR_DOCUMENTOS_A_PDF/
├── src/                    # Código fuente
│   └── pdf_consolidator/   # Módulo principal
├── tests/                  # Tests unitarios
│   ├── __init__.py
│   ├── conftest.py
│   └── test_utils.py
├── docs/                   # Documentación
├── scripts/                # Scripts de automatización
│   └── setup.bat          # Script de configuración inicial
├── config/                 # Archivos de configuración
│   ├── app_config.json
│   └── logging_config.json
├── data/                   # Datos de la aplicación
│   └── input/             # Datos de entrada
├── ARCHIVOS/              # [Usuario] Documentos de entrada
├── CONSOLIDADOS/          # [Salida] PDFs consolidados
├── TEMP_CONVERSION/       # [Temporal] Archivos de conversión
├── assets/                # Recursos gráficos
├── logs/                  # Archivos de log
├── .github/               # Configuración GitHub
│   └── copilot-instructions.md
├── main.py                # Punto de entrada de la aplicación
├── requirements.txt       # Dependencias de producción
├── requirements-dev.txt   # Dependencias de desarrollo
├── pyproject.toml         # Configuración del proyecto
├── .gitignore            # Archivos ignorados por Git
├── .pre-commit-config.yaml # Configuración pre-commit
├── LICENSE               # Licencia del proyecto
├── CHANGELOG.md          # Historial de cambios
└── Makefile              # Comandos de automatización
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con cobertura
pytest --cov=src

# Ejecutar tests específicos
pytest tests/test_conversion.py
```

## 🔧 Desarrollo

### Configuración del entorno de desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Instalar pre-commit hooks
pre-commit install

# Formatear código
black src/ tests/

# Verificar estilo
flake8 src/ tests/

# Verificar tipos
mypy src/
```

### Estructura de commits

- `feat:` - Nueva funcionalidad
- `fix:` - Corrección de bugs
- `refactor:` - Refactoring sin cambio de funcionalidad
- `docs:` - Cambios en documentación
- `style:` - Cambios de formato/estilo
- `test:` - Adición o modificación de tests
- `chore:` - Tareas de mantenimiento

## 📊 Logging

La aplicación genera logs detallados en la carpeta `logs/`:

- **Nivel INFO**: Operaciones normales y progreso
- **Nivel ERROR**: Errores de conversión y procesamiento
- **Rotación automática**: Archivos de máximo 1MB con 3 backups

## ⚠️ Limitaciones conocidas

- **Windows únicamente**: Dependiente de COM automation para MS Office
- **MS Office requerido**: Word y Excel deben estar instalados para conversión de documentos
- **Memoria**: Archivos muy grandes pueden consumir mucha memoria durante la conversión

## 🤝 Contribución

1. Fork el proyecto
2. Cree una rama para su feature (`git checkout -b feature/AmazingFeature`)
3. Commit sus cambios (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abra un Pull Request

## 📄 Licencia / Uso

**Uso interno de La Ascensión S.A. – Experiencia del Cliente.**

Este proyecto está desarrollado específicamente para uso interno de La Ascensión S.A. en el área de Experiencia del Cliente. El software está bajo la Licencia MIT para propósitos de desarrollo y mantenimiento. Ver el archivo `LICENSE` para más detalles técnicos de la licencia.

## 📞 Soporte

Para soporte técnico o reporte de bugs, por favor contacte:

- **Email**: <edwin.clavijo@laascension.com>
- **Issues**: [GitHub Issues](https://github.com/HarvLopez91/PY_UNIR_DOCUMENTOS_A_PDF/issues)

## 🏷️ Versión

**Versión actual**: 1.2.0

Ver [CHANGELOG.md](CHANGELOG.md) para el historial de cambios.