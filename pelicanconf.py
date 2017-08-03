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
SOCIAL = (
    ("Github", "https://github.com/flyte", "github"),
    ("Stack Overflow Careers", "https://stackoverflow.com/cv/ellis", "stack-overflow"),
    ("Mixcloud", "https://mixcloud.com/ellisfp", "mixcloud")
)

PROJECTS = [
    dict(
        name="pi-mqtt-gpio",
        url="https://github.com/flyte/pi-mqtt-gpio",
        description=("Expose the Raspberry Pi GPIO pins (and/or external IO mo"
                     "dules such as the PCF8574) to an MQTT server. This allow"
                     "s pins to be read and switched by reading or writing mes"
                     "sages to MQTT topics.")
    ),
    dict(
        name="pcf8574",
        url="https://github.com/flyte/pcf8574",
        description="A library for the pcf8574 I2C IO expander chip"
    ),
    dict(
        name="apcaccess",
        url="https://github.com/flyte/apcaccess",
        description=("Pure Python clone of <a href=\"http://linux.die.net/man/"
                     "8/apcaccess\">apcaccess</a> to allow programmatic use of"
                     " APC UPS status data.")
    ),
    dict(
        name="django-generic-counter",
        url="https://github.com/0x07Ltd/django-generic-counter",
        description=("A simple django app which contains a model to use as a c"
                     "ounter for anything you'd like.")
    )
]

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = "themes/elegant-custom"

LANDING_PAGE_ABOUT = dict(
    title="Beta not Best",
    details="""
    Freelance backend developer, DevOps and tech wrangler. Fan of home automation, embedded devices,
     sofas and hammocks.
    <p><em><a href="https://youtu.be/_fGujzulsas">Bit</a> is my spirit animal.</em></p>
    """
)

SITEMAP = {
    "format": "xml"
}

PLUGIN_PATHS = ["plugins"]
PLUGINS = ['sitemap', 'extract_toc', 'tipue_search']
# MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', 'headerid', 'toc']
MARKDOWN = dict(
    extension_configs={
        "codehilite": {"css_class": "highlight"},
        "extra": {},
        "headerid": {},
        "toc": {}
    }
)
COMMENTS_INTRO = "What do you think? Did I get something wrong? Could this be"\
                 " done better? Let me know below."
DIRECT_TEMPLATES = (("search", "index"))
SOCIAL_PROFILE_LABEL = "More of Me"
