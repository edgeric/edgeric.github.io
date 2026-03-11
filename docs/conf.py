# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0,os.path.abspath('..'))
import src.ModuleA
import src.ModuleB

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'EdgeRIC'
copyright = '2024, Ushasi Ghosh'
author = 'Ushasi Ghosh'
release = 'v0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_tabs.tabs',
    #'recommonmark',
    'myst_parser',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
    
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'myenv']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static', 'team_photos', 'demo_figs']
html_css_files = ['custom.css']
html_js_files = ['news-sidebar.js', 'demo-video.js', 'sidebar-clickable-titles.js']

# Furo theme options
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#0066cc",
        "color-brand-content": "#0066cc",
        "color-admonition-background": "rgba(0, 102, 204, 0.1)",
    },
    "dark_css_variables": {
        "color-brand-primary": "#4da6ff",
        "color-brand-content": "#4da6ff",
        "color-admonition-background": "rgba(77, 166, 255, 0.1)",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_buttons": ["view", "edit"],
    "source_repository": "https://github.com/yourusername/edgeric",
    "source_branch": "main",
    "source_directory": "docs/",
}

# Logo and favicon (uncomment and add files to _static/ to use)
# html_logo = "_static/logo.png"
# html_favicon = "_static/favicon.ico"

html_title = "EdgeRIC Documentation"
html_show_sourcelink = True