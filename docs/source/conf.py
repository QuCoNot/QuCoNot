# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here.
import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "QuCoNot"
copyright = "2022, Adam Glos, Ozlem Salehi"
author = "Adam Glos, Ozlem Salehi"
release = "0.01"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.viewcode",
    "sphinx.ext.coverage",
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    # "sphinx.ext.autodoc.typehints",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.viewcode",
    "sphinxcontrib.bibtex",
    "sphinx.ext.graphviz",
    "sphinx.ext.intersphinx",
    "sphinx_automodapi.automodapi",
    "sphinx_copybutton",
    "sphinx.ext.duration",
    "sphinx_togglebutton",
    "m2r2",
]
templates_path = ["_templates"]
# exclude_patterns = []
numpydoc_show_class_members = False
autosummary_generate = True
bibtex_bibfiles = ["refs.bib"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "sphinx_rtd_theme"
html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
html_theme_options = {
    "repository_url": "https://github.com/QuCoNot/QuCoNot",
    "use_repository_button": True,
    "use_issues_button": True,
}
html_logo = "logo.png"
html_title = "QuCoNot"