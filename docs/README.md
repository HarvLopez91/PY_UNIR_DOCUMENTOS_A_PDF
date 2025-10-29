# Documentación

Este directorio contiene toda la documentación del proyecto.

## Contenido

- `api.md` - Documentación de la API interna
- `user_guide.md` - Guía del usuario
- `development.md` - Guía de desarrollo
- `architecture.md` - Documentación de arquitectura

## Generar Documentación

La documentación puede ser generada automáticamente usando herramientas como Sphinx:

```bash
pip install sphinx sphinx-rtd-theme
sphinx-quickstart docs
sphinx-build -b html docs docs/_build
```