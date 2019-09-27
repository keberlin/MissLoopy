#!/usr/bin/python

import argparse

from iputils import *

parser = argparse.ArgumentParser(description='Lookup IP Address Geographical Location.')
parser.add_argument('ip', nargs='+', help='ip address to locate')
args = parser.parse_args()

for ip in args.ip:
  print ip, IpCountry(ip)
