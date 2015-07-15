#!/usr/bin/python

import os, sys, smtplib, email, re, tempfile

from logger import *

BASE_DIR = os.path.dirname(__file__)

# Look for the Diagnostic-Code which will show an email has bounced
def parse(msg):
  if msg.get('Diagnostic-Code'):
    recipient = msg.get('Original-Recipient')
    if not recipient:
      recipient = msg.get('Final-Recipient')
    if not recipient:
      logger.error('noreply: Could not find recipient in %s' % (msg))
      return None
    m = re.search(r'rfc822; *(.*)',recipient)
    if not m:
      logger.error('noreply: Did not understand recipient %s' % (recipient))
      return None
    return m.group(1)
  if msg.is_multipart():
    for part in msg.get_payload():
      recipient = parse(part)
      if recipient:
        return recipient
  return None

data = sys.stdin.read()

msg = email.message_from_string(data)

recipient = parse(msg)
if recipient:
  with open(os.path.join(BASE_DIR, 'bounced.log'), 'a') as file:
    if recipient[0] == '<':
      recipient = recipient[1:]
    if recipient[-1] == '>':
      recipient = recipient[:-1]
    file.write(recipient+'\n')
else:
  server = smtplib.SMTP('localhost')
  server.sendmail(msg.get('From'), 'admin', msg.as_string())
  server.quit()
