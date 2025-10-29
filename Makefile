# Makefile para PDF Consolidator
# Comandos de desarrollo y mantenimiento

.PHONY: help install install-dev test test-cov lint format clean build run setup

# Variables
PYTHON := python
PIP := pip
SRC_DIR := src
TEST_DIR := tests

help: ## Mostrar ayuda de comandos disponibles
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Configuración inicial del proyecto
	@echo "Configurando proyecto..."
	$(PYTHON) -m venv venv
	@echo "Activa el entorno virtual con: venv\\Scripts\\activate"

install: ## Instalar dependencias de producción
	$(PIP) install -r requirements.txt

install-dev: ## Instalar dependencias de desarrollo
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .
	pre-commit install

test: ## Ejecutar tests
	pytest $(TEST_DIR) -v

test-cov: ## Ejecutar tests con cobertura
	pytest $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing

lint: ## Verificar estilo de código
	flake8 $(SRC_DIR) $(TEST_DIR)
	mypy $(SRC_DIR)

format: ## Formatear código
	black $(SRC_DIR) $(TEST_DIR)
	black main.py

format-check: ## Verificar formato sin cambios
	black --check $(SRC_DIR) $(TEST_DIR) main.py

clean: ## Limpiar archivos temporales
	@echo "Limpiando archivos temporales..."
	rmdir /s /q __pycache__ 2>nul || true
	rmdir /s /q .pytest_cache 2>nul || true
	rmdir /s /q htmlcov 2>nul || true
	rmdir /s /q build 2>nul || true
	rmdir /s /q dist 2>nul || true
	rmdir /s /q *.egg-info 2>nul || true
	del /q .coverage 2>nul || true
	rmdir /s /q TEMP_CONVERSION\\* 2>nul || true

build: ## Construir distribución
	$(PYTHON) -m build

run: ## Ejecutar aplicación principal
	$(PYTHON) main.py

dev-install: install-dev ## Alias para install-dev

check: lint test ## Ejecutar todas las verificaciones

all: format lint test ## Ejecutar formato, lint y tests

# Comandos específicos de Windows
clean-win: ## Limpieza específica para Windows
	if exist __pycache__ rmdir /s /q __pycache__
	if exist .pytest_cache rmdir /s /q .pytest_cache
	if exist htmlcov rmdir /s /q htmlcov
	if exist build rmdir /s /q build
	if exist dist rmdir /s /q dist
	if exist .coverage del .coverage
	for /d %%i in (*.egg-info) do rmdir /s /q "%%i"