"""
PDF Consolidator - Módulo principal para consolidar documentos en PDF.

Este módulo proporciona funcionalidades para convertir y unir múltiples
documentos de diferentes formatos en un único archivo PDF.
"""

__version__ = "1.2.0"
__author__ = "La Ascensión S.A"
__email__ = "desarrollo@laascension.com"

from .main import main
from .converter import DocumentConverter
from .gui import ConsolidatorGUI

__all__ = ["main", "DocumentConverter", "ConsolidatorGUI"]