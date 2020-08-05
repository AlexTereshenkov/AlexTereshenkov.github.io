#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import socket
from datetime import datetime
from pathlib import Path

AUTHOR = 'Alexey Tereshenkov'
SITENAME = 'Software engineering notes'

# to support local preview
if 'LAPTOP' in socket.gethostname():
    SITEURL = 'https://localhost:8000'    
else:
    SITEURL = 'https://alextereshenkov.github.io'
SITETITLE = AUTHOR
SITESUBTITLE = 'Software engineering notes'

PATH = 'content'

TIMEZONE = 'GB'

DEFAULT_LANG = 'en'
THEME = Path.home().joinpath('blogging/pelican-themes/Flex/')

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('StackExchange', 'https://gis.stackexchange.com/users/14435/alex-tereshenkov?tab=profile'),         
         ('CodeQL for Python', 'https://blog.semmle.com/authors/alexey-tereshenkov/'),
         )
MAIN_MENU = True
MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

# Social widget
SOCIAL = (('github', 'https://github.com/alextereshenkov'),
          ('linkedin', 'https://www.linkedin.com/in/alexeytereshenkov/'),
          ('wordpress', 'https://tereshenkov.wordpress.com/'),
          )

DEFAULT_PAGINATION = 10

COPYRIGHT_NAME = AUTHOR
COPYRIGHT_YEAR = datetime.now().year
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True