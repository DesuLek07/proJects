# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SRRPM HelpDesk'
copyright = '2025, DesuLek07'
author = 'DesuLek07'
release = '1.5'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

extensions = [
    'sphinx.ext.autodoc',  # Para documentar automáticamente desde los docstrings
    'sphinx.ext.napoleon',  # Para soportar el estilo de Google en los docstrings
    'sphinx.ext.viewcode',  # Para enlazar al código fuente en la documentación
]

import os
import sys
sys.path.insert(0, os.path.abspath('../'))  

