@echo off
REM Script para generar ejecutable de distribución
REM Ejecutar tras cada cambio en el código

echo ========================================
echo  Generando Ejecutable PDF Consolidator
echo ========================================
echo.

REM Cambiar al directorio padre del script (directorio raíz del proyecto)
cd /d "%~dp0\.."

REM Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ERROR: No se encuentra main.py. Ejecute desde el directorio raíz del proyecto.
    echo Directorio actual: %CD%
    pause
    exit /b 1
)

REM Verificar que el entorno virtual esté activo
python -c "import sys; exit(0 if 'venv' in sys.prefix else 1)" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Activando entorno virtual...
    call venv\Scripts\activate.bat
)

REM Verificar PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando PyInstaller...
    pip install pyinstaller
)

REM Limpiar builds anteriores
echo 🧹 Limpiando builds anteriores...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "PDFConsolidator.spec" del PDFConsolidator.spec

REM Crear ícono si no existe
if not exist "assets\icon.ico" (
    echo ℹ️  Ícono no encontrado, usando configuración sin ícono
    set ICON_ARG=
) else (
    set ICON_ARG=--icon=assets\icon.ico
)

REM Generar ejecutable incluyendo assets y VERSION
echo 🔨 Generando ejecutable...
echo.
pyinstaller --onefile --windowed %ICON_ARG% --add-data "assets;assets" --add-data "VERSION;." --name="PDFConsolidator" main.py

if errorlevel 1 (
    echo ❌ ERROR: No se pudo generar el ejecutable
    pause
    exit /b 1
)

REM Crear estructura de distribución
echo 📁 Creando estructura de distribución...
if not exist "dist\data" mkdir "dist\data"
if not exist "dist\data\input" mkdir "dist\data\input"
if not exist "dist\data\output" mkdir "dist\data\output"
if not exist "dist\temp" mkdir "dist\temp"
if not exist "dist\logs" mkdir "dist\logs"

REM Copiar assets (imágenes) al directorio de distribución
echo 🖼️  Copiando assets...
if exist "assets" (
    if not exist "dist\assets" mkdir "dist\assets"
    copy "assets\*.*" "dist\assets\" >nul
    echo ✅ Assets copiados exitosamente
) else (
    echo ⚠️  Carpeta assets no encontrada, saltando copia
)

REM Copiar README de datos general
if exist "data\README.md" (
    copy "data\README.md" "dist\data\" >nul
) else (
    echo ⚠️  README.md de datos no encontrado, saltando copia
)

REM Crear README para usuario final
echo 📋 Creando documentación para usuario...
(
echo # PDF Consolidator - Aplicación de Usuario
echo.
echo ## Instrucciones de Uso
echo.
echo 1. Ejecute `PDFConsolidator.exe`
echo 2. Coloque sus documentos en la carpeta `data\input\`
echo 3. Complete los campos: Identificación, Cliente, Reembolso
echo 4. Haga clic en "Consolidar PDF"
echo 5. El archivo resultante estará en `data\output\`
echo.
echo ## Formatos Soportados
echo - PDF, Word (.doc/.docx^), Excel (.xlsx^), Imágenes (.jpg/.png/.tif^)
echo.
echo ## Soporte
echo - Contacto: edwin.clavijo@laascension.com
echo.
echo ## Versión
echo - Aplicación: PDF Consolidator v1.2.1
echo - Empresa: La Ascensión S.A.
echo - Fecha: %DATE%
) > "dist\README.md"

echo.
echo ✅ Ejecutable generado exitosamente en 'dist\'
echo.
echo 📋 Contenido de distribución:
dir /b dist
echo.
echo 🚀 Listo para distribución. Comprima la carpeta 'dist' y entregue al usuario.
echo.
pause