# Configuration file for the Sphinx documentation builder.

import os
import sys
# Agregamos la ruta del proyecto (ajusta si tu estructura cambia)
sys.path.insert(0, os.path.abspath('../../app'))

# -- Project information -----------------------------------------------------
project = 'Dongo'
copyright = '2025, Miguel Angel Leon Leon, Sara Camila Guarin Guerrero, Luis Alejandro Narvaez Talavera'
author = 'Miguel Angel Leon Leon, Sara Camila Guarin Guerrero, Luis Alejandro Narvaez Talavera'
release = '2.3'

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",   # Documenta automáticamente desde docstrings
    "sphinx.ext.napoleon",  # Soporte para Google/NumPy style
    "sphinx.ext.viewcode"   # Agrega enlaces al código fuente
]

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
