#!/usr/bin/python

import optparse, sys

from mlemail import *

parser = optparse.OptionParser()
parser.add_option("-s", "--subject", dest="subject", default="", help="subject text")

(options, args) = parser.parse_args()

def EmailBlock(email,subject,text):
  Email(email, subject, '<pre><h2>'+text+'</h2></pre>')

SUBJECT = options.subject
text = sys.stdin.read()
for TO in args:
  EmailBlock(TO, SUBJECT, text)
