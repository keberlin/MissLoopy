import argparse
import sys

from mlhtml import *

parser = argparse.ArgumentParser(description='Generate Static Pages.')
parser.add_argument('-s', metavar='title', nargs=1, help='title of page')
args = parser.parse_args()

data = sys.stdin.read()

d = {'text':data, 'title':args.s[0]}

print RenderY('static.html', d)
