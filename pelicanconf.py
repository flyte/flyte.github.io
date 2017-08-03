#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Ellis Percival'
SITENAME = u'Beta not Best'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = "themes/elegant-custom"

LANDING_PAGE_ABOUT = dict(
    title="Beta not Best",
    details="""
    <div>Freelance backend developer, DevOps and tech wrangler.</div>
    <hr />
    <ul>
      <li><a href="https://github.com/flyte">Github</a></li>
      <li><a href="https://stackoverflow.com/cv/ellis">Stack Overflow Careers CV</a></li>
    </ul>
    <hr />
    """
)
