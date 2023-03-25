# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'mkpkg'
copyright = '2023, Perry Bunn'
author = 'Perry Bunn'
release = '0.1.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'autoapi.extension',
    'sphinx.ext.inheritance_diagram',
    'autoapi.sphinx'
]

autoapi_dirs = ['../../mkpkg/']
autoapi_root = 'autoapi'
autoapi_keep_files = False
autoapi_add_toctree_entry = False
autoapi_options = ['members', 'undoc-members', 'show-inheritance',
                   'special-members']
# autoapi_options = ['members', 'undoc-members', 'private-members',
#                    'show-inheritance', 'special-members']
autoapi_ignore = ['*configs.py']

templates_path = ['_templates']
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'classic'
html_sidebars = {'**': ['globaltoc.html',
                        'relations.html',
                        'sourcelink.html',
                        'searchbox.html']
                 }
html_static_path = ['_static']

# -- Numpy style configuration --
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# -- Options for todo extension --
# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
