@echo off
setlocal EnableDelayedExpansion
REM Script de configuración inicial para PDF Consolidator
REM Ejecutar desde el directorio raíz del proyecto

echo ========================================
echo  Configuración PDF Consolidator
echo ========================================
echo.

REM Cambiar al directorio padre del script
cd /d "%~dp0\.."

REM Verificar que estamos en el directorio correcto
if not exist "main.py" (
    echo ERROR: No se encuentra main.py. Ejecute desde el directorio raíz del proyecto.
    echo Directorio actual: %CD%
    pause
    exit /b 1
)

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor instale Python 3.8 o superior desde https://python.org
    pause
    exit /b 1
)

echo ✓ Python detectado
python --version

REM Verificar archivo requirements.txt
if not exist "requirements.txt" (
    echo ERROR: No se encuentra requirements.txt
    echo Asegúrese de que el archivo existe en el directorio raíz
    pause
    exit /b 1
)

REM Limpiar entorno virtual existente si existe
if exist "venv" (
    echo Eliminando entorno virtual existente...
    rmdir /s /q venv
)

REM Crear entorno virtual
echo.
echo Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

echo ✓ Entorno virtual creado

REM Activar entorno virtual
echo.
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo.
echo Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo.
echo Instalando dependencias de producción...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo ✓ Dependencias de producción instaladas

REM Instalar dependencias de desarrollo (opcional)
if exist "requirements-dev.txt" (
    set /p install_dev="¿Instalar dependencias de desarrollo? (y/N): "
    if /i "!install_dev!"=="y" (
        echo.
        echo Instalando dependencias de desarrollo...
        pip install -r requirements-dev.txt
        if errorlevel 1 (
            echo ERROR: No se pudieron instalar las dependencias de desarrollo
            echo Continuando con solo las dependencias de producción...
        ) else (
            echo ✓ Dependencias de desarrollo instaladas
        )
    )
) else (
    echo requirements-dev.txt no encontrado, saltando dependencias de desarrollo
)

REM Crear directorios necesarios
echo.
echo Creando estructura de directorios...
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp
if not exist "data" mkdir data
if not exist "data\input" mkdir data\input
if not exist "data\output" mkdir data\output
if not exist "assets" mkdir assets
echo ✓ Estructura de directorios creada

REM Verificar que la aplicación puede ejecutarse
echo.
echo Verificando instalación...
python -c "import main; print('✓ Aplicación verificada correctamente')" 2>nul
if errorlevel 1 (
    echo ⚠️  Advertencia: Verificación de la aplicación falló
    echo La instalación puede estar incompleta
) else (
    echo ✓ Aplicación lista para usar
)

echo.
echo ========================================
echo  Configuración completada exitosamente
echo ========================================
echo.
echo Para usar la aplicación:
echo 1. Activa el entorno virtual: venv\Scripts\activate
echo 2. Ejecuta la aplicación: python main.py
echo.
echo Para generar ejecutable:
echo - Ejecuta: scripts\build_exe.bat
echo.
echo Archivos importantes:
echo - main.py: Aplicación principal
echo - requirements.txt: Dependencias de producción
echo - assets\: Recursos gráficos (logos)
echo - data\: Directorio de trabajo (input/output)
echo.
pause