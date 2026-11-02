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
copyright = '2024-2026, Ushasi Ghosh and WCSNG, UC San Diego'
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
    'sphinx_sitemap',
    'sphinxext.opengraph',
]

# Generate HTML anchors for markdown headings (h1-h4) so in-page links
# like [text](#some-heading) resolve.
myst_heading_anchors = 4

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
    
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'myenv']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static', 'team_photos', 'demo_figs', 'pics']
html_css_files = ['custom.css', 'news.css']
html_js_files = ['sidebar-brand-logos.js', 'news-sidebar.js', 'demo-video.js', 'sidebar-clickable-titles.js', 'sidebar-expand-collapse.js']

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
    "source_repository": "https://github.com/edgeric/edgeric.github.io",
    "source_branch": "main",
    "source_directory": "docs/",
}

# Logo and favicon (uncomment and add files to _static/ to use)
# html_logo = "_static/logo.png"
# html_favicon = "_static/favicon.ico"

html_title = "EdgeRIC: Real-Time AI-RAN and Open RAN Controller"

# edgeric.ucsd.edu is the canonical domain; edgeric.github.io is a mirror.
# This also adds <link rel="canonical"> to every page.
html_baseurl = "https://edgeric.ucsd.edu/"
html_extra_path = ["robots.txt", ".htaccess"]

# Sitemap
sitemap_url_scheme = "{link}"
sitemap_excludes = [
    "search.html",
    "genindex.html",
    "py-modindex.html",
    "404.html",
    "5g-testbed.html",
    "projects/lens.html",
    "projects/prism.html",
    "projects/cloud-gaming.html",
]

# OpenGraph
ogp_site_url = "https://edgeric.ucsd.edu/"
ogp_site_name = "EdgeRIC"
ogp_image = "https://edgeric.ucsd.edu/_static/edgeric-intro.png"
ogp_description_length = 160
ogp_social_cards = {"enable": False}
html_show_sourcelink = True

def _root_canonical(app, pagename, templatename, context, doctree):
    # The homepage lives at /, not /index.html
    if pagename == "index":
        context["pageurl"] = html_baseurl


def setup(app):
    app.connect("html-page-context", _root_canonical)
