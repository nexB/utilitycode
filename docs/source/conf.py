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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "UtilityCode"
copyright = "nexB Inc."
author = "nexB Inc."

version = "1.0.0"
# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.intersphinx"]

master_doc = "index"

intersphinx_mapping = {
    "scancode-toolkit": ("https://scancode-toolkit.readthedocs.io/en/latest/", None),
    "scancode-workbench": (
        "https://scancode-workbench.readthedocs.io/en/develop/",
        None,
    ),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"

# This adds to the levels displayed in the sidebar but the indent is wrong and expand/collapse doesn't work for the additional nodes.
# It's a known issue: see https://stackoverflow.com/questions/14477396/how-to-expand-all-the-subsections-on-the-sidebar-toctree-in-sphinx and https://github.com/readthedocs/sphinx_rtd_theme/issues/455
# html_theme_options = {
#     'navigation_depth': 6,
# }

# 3/29/2022 Tuesday 11:05:48 AM.  From JMH RTD.
html_theme_options = {
    "canonical_url": "",
    "analytics_id": "UA-XXXXXXX-1",
    "logo_only": False,
    # 'version_selector': True,
    # 'prev_next_buttons_location': 'bottom',
    # 'prev_next_buttons_location': 'top',
    "prev_next_buttons_location": "both",
    # 'style_external_links': False,
    # 'style_external_links': True,
    # 'style_nav_header_background': 'white',
    # Toc options
    # 'collapse_navigation': True,
    "collapse_navigation": False,
    # 'sticky_navigation': True,
    "sticky_navigation": False,
    # 'navigation_depth': 4,
    "navigation_depth": -1,
    "includehidden": True,
    "titles_only": False,
}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_context = {
    "display_github": True,
    "github_user": "nexB",
    "github_repo": "utilitycode",
    "github_version": "develop",  # branch
    "conf_py_path": "/docs/source/",  # path in the checkout to the docs root
}

html_css_files = [
    # '_static/theme_overrides.css'
    # 'theme_overrides.css',
    # 'theme_overrides-skeleton-2022-03-28.css',
    "theme_overrides-skeleton-2022-03-28-updated.css"
]

html_js_files = [
    "js/custom.js",
]

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = True

# Define CSS and HTML abbreviations used in .rst files.  These are examples.
# .. role:: is used to refer to styles defined in _static/theme_overrides.css
# and is used like this: :red:`text`
rst_prolog = """
.. # define a hard line break for HTML
.. |br| raw:: html

   <br />

.. # define a style for a toctree heading -- see, e.g., the top of index.rst for usage example
.. role:: toc

.. # or replace with:

.. |div-page-outline| raw:: html

   <div class="div_page_outline">
   Page outline
   </div>


.. |div-section-outline| raw:: html

   <div class="div_section_outline">
   Table of contents (this section)
   </div>


.. |div-rtd-outline| raw:: html

   <div class="div_rtd_outline">
   Table of contents (entire RTD)
   </div>

.. role:: yellow-background

.. role:: green-background

.. role:: blue-background

.. role:: red-background

"""

# Convert a double-dash "--" into a typographical en-dash "–":
# (Omitting the smartquotes from this conf.py has the same effect as setting it to True)
# smartquotes = True
# Do not change the display of a double-dash:
smartquotes = False
# -- Options for LaTeX output -------------------------------------------------

latex_elements = {"classoptions": ",openany,oneside"}
