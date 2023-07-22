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
PROJECTS_TITLE = "Hobby projects"
PROJECTS = [
    {
    'name': 'Building Python with Pants',
    'url': 'https://github.com/AlexTereshenkov/cheeseshop-query',
    'description': ('Build a Python project with PyPI dependencies using Pants')},
    {
    'name': 'Building Java with Bazel',
    'url': 'https://github.com/AlexTereshenkov/java-bazel-build-example',
    'description': ('Build a Java project with Maven dependencies using Bazel')},
    {
    'name': 'Pybutler',
    'url': 'https://github.com/AlexTereshenkov/pybutler',
    'description': ('Java interactive CLI tool for scaffolding Python 3 project unit tests using ANTLR')},
    {
    'name': 'Shapy',
    'url': 'https://github.com/AlexTereshenkov/shapy',
    'description': ('Java CLI tool to read ESRI shapefiles binary data and metadata')},
    {
    'name': 'GDBee',
    'url': 'https://github.com/AlexArcPy/GDBee',
    'description': ('PyQt5 desktop SQL editor for spatial geodatabases')},
    {
    'name': 'Registrant',
    'url': 'https://github.com/AlexArcPy/registrant',
    'description': 'Generator of HTML reports about the contents of spatial geodatabases'},    
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
