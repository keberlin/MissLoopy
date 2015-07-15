#!/usr/bin/python

import sys, argparse

from html import *
from mlhtml import *

parser = argparse.ArgumentParser(description='Construct HTML pages from templates.')
parser.add_argument('-s', metavar='subtitle', nargs=1, required=False, help='override subtitle')
args = parser.parse_args()

dict = {}
if 'subtitle' in args:
  dict['subtitle'] = args.subtitle[0]

dict['text'] = sys.stdin.read()

print RenderY('static.html', dict)
