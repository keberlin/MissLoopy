import fileinput, re
from iputils import *

def IpSub(m):
  return IpCountry(m.group(1))

for line in fileinput.input():
  print re.sub(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', IpSub, line),
