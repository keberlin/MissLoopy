import os
import sys
from html import *

import jinja2

BASE_DIR = os.path.dirname(__file__)

def url_for(endpoint, **values):
  return os.path.join('/', endpoint, values['filename'])

loader = jinja2.FileSystemLoader(searchpath=os.path.join(BASE_DIR, "templates"))
env = jinja2.Environment(loader=loader)
env.globals.update(url_for=url_for)

def Redirect(url):
  print 'Location: %s' % (url)
  print
  sys.exit(0)

def RenderY(template,dict=None):
  d = html_defaults()
  if dict: d.update(dict)
  template = env.get_template(template)
  return template.render(**d).encode('utf-8')
