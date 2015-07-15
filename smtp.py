#!/usr/bin/python

import sys, re, email

debug = False

sender = ''
subject = ''
message = ''
images = []

def parse(msg,indent=0):
  global debug
  global sender
  global subject
  global message
  global images
  if debug:
    for key in msg.keys():
      print '%s%s: %s' % (' '*indent, key, msg[key])
  if 'From' in msg.keys():
    sender = msg['From']
  if 'Subject' in msg.keys():
    subject = msg['Subject']
  if msg.is_multipart():
    if debug:
      print '%smultipart..' % (' '*indent)
    for part in msg.get_payload():
      parse(part,indent+2)
  elif msg.get_content_type() == 'text/plain':
    if debug:
      print '%s%s' % (' '*indent, re.sub(r'\n',r' ',msg.get_payload()[:100]))
    message = msg.get_payload()
    if re.search(r'- forwarded message -', message, re.IGNORECASE):
      lines = []
      capture = False
      for line in message.split('\n'):
        if re.search(r'^-+ forwarded message -+$', line, re.IGNORECASE):
          capture = True
          continue
        elif re.search(r'^-+$', line):
          break
        if capture and len(line):
          lines.append(line)
      parse(email.message_from_string('\n'.join(lines)))
  elif msg.get_content_type() == 'image/jpeg':
# data = cStringIO.StringIO()
# im.save(data, 'JPEG')
# message = 'data:image/jpg;base64,' + base64.b64encode(data.getvalue())
    images.append('<img src="data:image/jpg;base64,%s">' % msg.get_payload())
  else:
    if debug:
      print '%s%s' % (' '*indent, re.sub(r'\n',r' ',msg.get_payload()[:100]))
  return None

msg = email.message_from_file(sys.stdin)
parse(msg)

print '<html><body>'
print '<b>From:</b>', sender, '<br>'
print '<b>Subject:</b>', subject, '<br>'
print message, '<br>'
for image in images:
  print image
print '</body><html>'
