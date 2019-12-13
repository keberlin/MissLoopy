import sys, email, re

from logger import *

debug = False

def parse(msg,indent=0):
  if debug:
    for key in msg.keys():
      print '%s%s: %s' % (' '*indent, key, msg[key])
  if 'Diagnostic-Code' in msg.keys():
    #print 'Unrecognised:', [(key,msg[key]) for key in msg.keys()]
    text = msg['Diagnostic-Code'].lower()
    if 'Original-Recipient' in msg.keys():
      recipient = msg['Original-Recipient'].lower()
    else:
      recipient = msg['Final-Recipient'].lower()
    m = re.search(r'rfc822; *(.*)',recipient)
    #logger.info('AUTO '+recipient+' '+text)
    return m.group(1)
  if msg.is_multipart():
    if debug:
      print '%smultipart..' % (' '*indent)
    for part in msg.get_payload():
      str = parse(part,indent+2)
      if str:
        return str
  elif msg.get_content_type() == 'text/plain':
    if debug:
      print '%stext/plain..' % (' '*indent)
      print '%s%s' % (' '*indent, re.sub(r'\n',r' ',msg.get_payload()))
  return None
