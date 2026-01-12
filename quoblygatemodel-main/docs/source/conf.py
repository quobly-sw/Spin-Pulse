# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "SpinPulse"
copyright = "2025, Quobly"
author = "Quobly"
release = "2025, Quobly"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # "sphinx.ext.autodoc",  # core: import modules, read docstrings
    "sphinx.ext.napoleon",  # NumPy / Google style docstrings
    "sphinx.ext.autosummary",  # auto-generate API stub pages
    "sphinx.ext.viewcode",  # link to highlighted source code
    "autoapi.extension",  # AutoAPI for automatic API documentation
    "myst_nb",  # For notebooks integration
    "sphinx_design",  # For better design blocks
    "sphinx_copybutton",  # For copy buttons in code blocks
    "sphinx.ext.intersphinx",  # Link to other projects documentation
    # "sphinx.ext.extlinks",  # to be added when github repo is done
    # "sphinx.ext.linkcode",  # to be added when github repo is done
]

numfig = True

templates_path = ["_templates"]

# -- Link to other documentation -----------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- Napoleon configuration ---------------------------------------------------
napoleon_google_docstring = True
napoleon_include_special_with_doc = True
napoleon_use_param = True
napoleon_attr_annotations = False

# -- AutoAPI configuration ------------------------------------------------

napoleon_google_docstring = True
autodoc_class_signature = "mixed"
autodoc_typehints = "description"  # show type hints in descriptions
autodoc_typehints_format = "fully-qualified"  # use fully qualified names

autoapi_dirs = ["../../src/spin_pulse/"]
autoapi_root = "autoapi"
autoapi_add_toctree_entry = False

autoapi_options = ["members", "undoc-members", "show-inheritance", "imported-members"]
autoapi_options = [
    "members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
    "undoc-members",
]

suppress_warnings = ["ref.python"]

# autoapi_ignore = [
#     "*transpilation/pulse_circuit.py",        # ignore ce module interne
#     "*transpilation/hardware_specs.py",       # si tu as un alias haut niveau
#     "*transpilation/instructions/pulse_instruction.py",
# ]

autoapi_python_class_content = "both"
autoapi_member_order = "bysource"
autoapi_keep_files = True
autoapi_generate_api_docs = True
autoapi_template_dir = "_templates/autoapi"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "pydata_sphinx_theme"
html_theme = "furo"
html_title = "SpinPulse"
html_show_sourcelink = False
# html_short_title = "API"s
html_theme_options = {
    "sidebar_hide_name": True,
    "light_css_variables": {
        # "color-brand-primary": "hsl(45, 80%, 45%)",
        "color-brand-primary": "hsl(210, 50%, 50%)",
        "color-brand-content": "hsl(210, 50%, 50%)",
        # "font-stack": "Atkinson Hyperlegible, sans-serif",
        # "font-stack--monospace": "Spline Sans Mono, monospace",
        # "font-stack--headings": "Spline Sans Mono, monospace",
    },
    "dark_css_variables": {
        "color-brand-primary": "hsl(210, 50%, 60%)",
        "color-brand-content": "hsl(210, 50%, 60%)",
    },
    "light_logo": "SpinPulse.png",
    "dark_logo": "SpinPulse.png",
}

# pygments_style = "_pygments_light.MarianaLight"
# pygments_dark_style = "_pygments_dark.MarianaDark"

html_static_path = ["_static"]
# For Sphinx (not strictly used by pydata, but okay to keep)
# html_logo = "_static/SpinPulse.png"

# css files are relative to _static/, so no "_static/" here
html_css_files = ["custom.css"]


# -- Options for notebook execution -------------------------------------------
nb_execution_mode = "off"
myst_heading_anchors = 4
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
]
