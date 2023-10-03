import datetime
import random
import re
import urllib

from detectmobilebrowser import *

TITLE    = 'Miss Loopy'
SUBTITLE = '100% Free Online Dating Site'
YEAR     = datetime.date.today().year

DOMAIN   = 'MissLoopy.com'
URL      = 'www.' + DOMAIN.lower()
WWW      = 'http://' + URL

PROMO    = '100% Free Online Dating Site'

#PUBLISHERS = ['bannerplay','amazon-us-1','amazon-us-2','amazon-us-3','revenuehits']
PUBLISHERS = ['google']

def html_defaults(user_agent=None):
  return {
    'domain':    DOMAIN,
    'www':       WWW,
    'title':     TITLE,
    'subtitle':  SUBTITLE,
    'year':      YEAR,
    'promo':     PROMO,
    'banner':    PUBLISHERS[random.randint(0,len(PUBLISHERS)-1)] + '-banner',
    'publisher': PUBLISHERS[random.randint(0,len(PUBLISHERS)-1)],
    'is_mobile': is_mobile_browser(user_agent)
  }

def HtmlLink(text,link):
  return '<a href="%s">%s</a>' % (link, text)

def HtmlImage(file,attrs=''):
  return '<img src="%s" %s>' % (file, attrs)

def HtmlOption(value,text):
  return '<option value="%s">%s</option>' % (value, text)

def HtmlButton(text,attrs=''):
  return '<button %s>%s</button>' % (attrs, text)
