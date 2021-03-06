# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.append(os.path.abspath('../sphinx_rtd_dark_mode'))
sys.path.append(os.path.abspath('../../'))


# -- Project information -----------------------------------------------------

project = 'GMM-Demux'
copyright = '2019 - 2022 CHPGenetics'
author = 'Hongyi Xin'

# The full version, including alpha/beta/rc tags
release = '1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	'myst_parser',
	'sphinx.ext.intersphinx',
	'sphinx.ext.autosummary',
	'sphinx_rtd_dark_mode',
	'sphinx.ext.autosectionlabel'
]

# intersphinx_mapping = {
# 	'numpy': ('http://docs.scipy.org/doc/numpy/', None),
# 	'int': ('https://docs.python.org/3/library/functions.html#int', None)
# }

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'navigation_depth': 4,
}
html_show_sphinx = False
html_show_sourcelink = False
pygments_style = "sphinx"
html_logo = '_static/favicon.ico'
html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']