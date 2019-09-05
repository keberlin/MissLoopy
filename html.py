import re, datetime, urllib, random

from detectmobilebrowser import *

TITLE    = 'Miss Loopy'
SUBTITLE = '100% Free Online Dating Site'
YEAR     = datetime.date.today().year

HOST = 'missloopy'

PROMO    = '100% Free Online Dating Site'

#PUBLISHERS = ['bannerplay','amazon-us-1','amazon-us-2','amazon-us-3','revenuehits']
PUBLISHERS = ['google']

def html_defaults(host,user_agent=None):
  DOMAIN   = re.search('%s.*'%HOST,host,re.IGNORECASE).group()
  URL      = 'www.' + DOMAIN.lower()
  WWW      = 'http://' + URL

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
