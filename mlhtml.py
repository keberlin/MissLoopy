import datetime
import os
import random
import re
import sys
import urllib

import jinja2

from detectmobilebrowser import *

BASE_DIR = os.path.dirname(__file__)

TITLE = "Miss Loopy"
SUBTITLE = "100% Free Online Dating Site"
YEAR = datetime.date.today().year

DOMAIN = "MissLoopy.com"
URL = "www." + DOMAIN.lower()
WWW = "http://" + URL

PROMO = "100% Free Online Dating Site"

# PUBLISHERS = ['bannerplay','amazon-us-1','amazon-us-2','amazon-us-3','revenuehits']
PUBLISHERS = ["google"]


def html_defaults(user_agent=None):
    return {
        "domain": DOMAIN,
        "www": WWW,
        "title": TITLE,
        "subtitle": SUBTITLE,
        "year": YEAR,
        "promo": PROMO,
        "banner": PUBLISHERS[random.randint(0, len(PUBLISHERS) - 1)] + "-banner",
        "publisher": PUBLISHERS[random.randint(0, len(PUBLISHERS) - 1)],
        "is_mobile": is_mobile_browser(user_agent),
    }


def HtmlLink(text, link):
    return '<a href="%s">%s</a>' % (link, text)


def HtmlImage(file, attrs=""):
    return '<img src="%s" %s>' % (file, attrs)


def HtmlOption(value, text):
    return '<option value="%s">%s</option>' % (value, text)


def HtmlButton(text, attrs=""):
    return "<button %s>%s</button>" % (attrs, text)


def url_for(endpoint, **values):
    return os.path.join("/", endpoint, values["filename"])


loader = jinja2.FileSystemLoader(searchpath=os.path.join(BASE_DIR, "templates"))
env = jinja2.Environment(loader=loader)
env.globals.update(url_for=url_for)


def Redirect(url):
    print("Location: %s" % (url))
    print
    sys.exit(0)


def RenderY(template, dict=None):
    d = html_defaults()
    if dict:
        d.update(dict)
    template = env.get_template(template)
    return template.render(**d)
