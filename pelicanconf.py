#!/usr/bin/env python
from __future__ import unicode_literals
import socket
from datetime import datetime
from pathlib import Path

GOOGLE_ANALYTICS = 'UA-177875539-1'

AUTHOR = 'Alexey Tereshenkov'
SITENAME = 'Alexey Tereshenkov'

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.smarty': {},
        'markdown.extensions.toc' :{'permalink' : 'true'},
        'markdown.extensions.footnotes': {},
    },
    'output_format': 'html5',
}

# to do a local preview, run "pelican --listen -p <port>"
SITEURL = 'https://alextereshenkov.github.io'
LANDING_PAGE_TITLE = 'Software engineering notes'

TIMEZONE = 'GB'
DEFAULT_LANG = 'en'

THEME = Path.home().joinpath('blogging/elegant').as_posix()
PLUGIN_PATHS = [Path.home().joinpath('blogging/pelican-plugins').as_posix()]

# tipue_search - to enable search on the webpage
# liquid_tags - to place code from files into the .md file
PLUGINS = ['tipue_search', 'sitemap', 'liquid_tags.include_code', 'extract_toc']
DIRECT_TEMPLATES = ('index', 'tags', 'categories','archives', 'search', '404')

# landing page items
PROJECTS_TITLE = "My projects"
PROJECTS = [{
    'name': 'Pybutler',
    'url': 'https://github.com/AlexTereshenkov/pybutler',
    'description': ('Java interactive CLI tool for scaffolding Python 3 project unit tests using ANTLR')},
    {
    'name': 'Shapy',
    'url': 'https://github.com/AlexTereshenkov/shapy',
    'description': ('Java CLI tool to read ESRI shapefiles binary data and metadata')},
    {
    'name': 'CodeQL for Python',
    'url': 'https://blog.semmle.com/authors/alexey-tereshenkov/',
    'description': ('My posts about using CodeQL for Python projects')},
    {
    'name': 'Geospatial blog',
    'url': 'https://tereshenkov.wordpress.com/',
    'description': ('My blog about programming and managing GIS software and services')},
    {
    'name': 'GDBee',
    'url': 'https://github.com/AlexArcPy/GDBee',
    'description': ('PyQt5 desktop SQL editor for spatial geodatabases')},
    {'name': 'Registrant',
    'url': 'https://github.com/AlexArcPy/registrant',
    'description': 'Generator of HTML reports about the contents of spatial geodatabases'},
    {'name': 'Python for GIS',
    'url': 'https://github.com/AlexArcPy/python-for-gis-progression-path',
    'description': ('Progression path for a GIS analyst who wants to become proficient ' 
                   'in using Python for GIS: from apprentice to guru')},
    
    ]

SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.5,
        "indexes": 0.5,
        "pages": 0.5
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly"
    }
}
