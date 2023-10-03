#!/usr/bin/python

import email
import logging
import os
import re
import smtplib
import sys
import tempfile

BASE_DIR = os.path.dirname(__file__)

# Look for the Diagnostic-Code which will show an email has bounced
def parse(msg):
  if msg.get('Diagnostic-Code'):
    recipient = msg.get('Original-Recipient')
    if not recipient:
      recipient = msg.get('Final-Recipient')
    if not recipient:
      logging.error('ERROR: noreply: Could not find recipient in %s' % (msg))
      return None
    m = re.search(r'rfc822; *(.*)',recipient)
    if not m:
      logging.error('ERROR: noreply: Did not understand recipient %s' % (recipient))
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

bounced = parse(msg)
if bounced:
  with open(os.path.join(BASE_DIR, 'bounced.log'), 'a') as file:
    if bounced[0] == '<':
      bounced = bounced[1:]
    if bounced[-1] == '>':
      bounced = bounced[:-1]
    file.write(bounced+'\n')
else:
  server = smtplib.SMTP('localhost')
  server.sendmail(msg.get('From'), 'admin', msg.as_string())
  server.quit()
