import fileinput
import re

from utils import *

EMAIL_PATTERN = r'([A-Z0-9][A-Z0-9_.-]*)[@#]([A-Z0-9]+)\.([A-Z]+(?:\.[A-Z]+)*)'

addresses = set()
for line in fileinput.input():
  message = line.decode('utf-8','ignore')

  for address in re.findall(EMAIL_PATTERN, message, re.IGNORECASE):
    for i in range(len(address)):
      if len(address[i]):
        break
    name   = re.sub(r'.*\.\.','',address[i].lower())
    domain = address[i+1].lower()
    if domain in ['yaho','yahu','yahuu','ym']:
      domain = 'yahoo'
    if domain in ['fb']:
      domain = 'facebook'
    ext    = address[i+2].lower()
    if ext in ['c','cm','om','c.o.m']:
      ext = 'com'
    if len(ext) == 0:
      ext = 'com'
    addresses.add(name+'@'+domain+'.'+ext)

for address in addresses:
  print address.encode('utf-8')
