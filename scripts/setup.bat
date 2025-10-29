@echo off
REM Script de configuración inicial para PDF Consolidator
REM Ejecutar como administrador si es necesario

echo ========================================
echo  Configuración PDF Consolidator
echo ========================================
echo.

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
set /p install_dev="¿Instalar dependencias de desarrollo? (y/N): "
if /i "%install_dev%"=="y" (
    echo.
    echo Instalando dependencias de desarrollo...
    pip install -r requirements-dev.txt
    pip install -e .
    echo ✓ Dependencias de desarrollo instaladas
    
    echo.
    echo Configurando pre-commit hooks...
    pre-commit install
    echo ✓ Pre-commit hooks configurados
)

REM Crear directorios necesarios
echo.
echo Creando estructura de directorios...
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp
if not exist "data" mkdir data
if not exist "data\input" mkdir data\input
if not exist "data\output" mkdir data\output
echo ✓ Estructura de directorios creada

echo.
echo ========================================
echo  Configuración completada exitosamente
echo ========================================
echo.
echo Para usar la aplicación:
echo 1. Activa el entorno virtual: venv\Scripts\activate
echo 2. Ejecuta la aplicación: python main.py
echo.
echo Para desarrollo:
echo - Formatear código: make format
echo - Ejecutar tests: make test
echo - Verificar código: make lint
echo.
pause