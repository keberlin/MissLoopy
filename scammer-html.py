import email
import re
import sys
from xml.sax.saxutils import escape

from bs4 import BeautifulSoup
from mlhtml import *

debug = False

# Concat all lines ending with =
def Concat(text,sep='\n'):
  lines = []
  buffer = ''
  for line in text.split('\n'):
    if len(line) and line[-1] == '=':
      buffer += line[:-1]
    elif len(buffer):
      lines.append(buffer+line)
      buffer = ''
    else:
      lines.append(line)
  return sep.join(lines)

# Convert all =XX to ascii chars
def Convert(text):
  def Conv(m):
    c = eval('0x'+m.group(1))
    return str(chr(c))
  return re.sub('=([0-9A-F][0-9A-F])',Conv,text)

def walker(soup):
  if soup.name is not None:
    for child in soup.children:
      if child.name:
        attrs = []
        for name, value in child.attrs.items():
          if isinstance(value,list):
            attrs.append(name+'="'+' '.join(value)+'"')
          else:
            attrs.append(name+'="'+value+'"')
        if len(attrs):
          yield '<'+child.name+' '+' '.join(attrs)+'>'
        else:
          yield '<'+child.name+'>'
      elif child.string:
        yield escape(child.string.strip())
      for string in walker(child):
        yield string
      if child.name:
        if child.name != 'br':
          yield '</'+child.name+'>'

dict = {}
images = []

def parse(msg,indent=0):
  global debug, dict, images
  if debug:
    for key in msg.keys():
      print '%s%s: %s' % (' '*indent, key, msg[key])
  rawparam = msg.get('From')
  if rawparam:
    dict['sender'] = escape(rawparam)
  rawparam = msg.get('Date')
  if rawparam:
    dict['date'] = rawparam
  rawparam = msg.get('Subject')
  if rawparam:
    dict['subject'] = escape(rawparam)
  if msg.is_multipart():
    if debug:
      print '%smultipart..' % (' '*indent)
    for part in msg.get_payload():
      parse(part,indent+2)
  else:
    if debug:
      print '%s%s' % (' '*indent, re.sub(r'\n',' ',msg.get_payload()[:100]))
    if msg.get_content_type() == 'text/plain':
      text = msg.get_payload(decode=True)
      with open('plain.txt', 'w') as f:
        f.write(text)
      text = text.decode('utf-8', 'ignore')
      lines = []
      overflow = False
      for line in text.split('\n'):
        # Extract forwarding info
        if re.search('^-+ *Forwarded message *-+$', line):
          continue
        m = re.search('^From: *(.*)$', line)
        if m:
          attr = 'sender'
          dict[attr] = m.group(1)
          overflow = True
          continue
        m = re.search('^Date: *(.*)$', line)
        if m:
          attr = 'date'
          dict[attr] = m.group(1)
          overflow = True
          continue
        m = re.search('^Subject: *(.*)$', line)
        if m:
          attr = 'subject'
          dict[attr] = m.group(1)
          overflow = True
          continue
        m = re.search('^To: *(.*)$', line)
        if m:
          attr = None
          overflow = True
          continue
        m = re.search('^Cc: *(.*)$', line)
        if m:
          attr = None
          overflow = True
          continue
        # Remove the trailing forwarding info
        if re.search('^_+$', line):
          break
        if re.search('-+ *Original Message *-+', line):
          break
        if re.search('^ *On ', line):
          break
        if overflow:
          if len(line) == 0:
            overflow = False
          elif attr:
            dict[attr] += ' '+line
          continue
        lines.append(line)
      dict['msg'] = '<br>'.join(lines)
    elif msg.get_content_type() == 'text/html':
      text = msg.get_payload(decode=True)
      with open('html.txt', 'w') as f:
        f.write(text)
      soup = BeautifulSoup(text, "html.parser")
      dict['msg'] = ''
      overflow = False
      for string in walker(soup):
        if re.search('^-+ *Forwarded message *-+$', string):
          continue
        if re.search('^<hr', string):
          break
        if re.search('-+ *Original Message *-+', string):
          break
        if re.search('^-+$', string):
          break
        if re.search('^ *On (Mon|Tue|Wed|Thu|Fri|Sat|Sun)', string):
          break
        m = re.search('^ *From: *(.*)', string)
        if m:
          attr = 'sender'
          dict[attr] = m.group(1)
          overflow = True
          continue
        m = re.search('^ *Date: *(.*)', string)
        if m:
          attr = 'date'
          dict[attr] = m.group(1)
          overflow = True
          continue
        m = re.search('^ *Subject: *(.*)', string)
        if m:
          attr = 'subject'
          dict[attr] = m.group(1)
          overflow = True
          continue
        m = re.search('^ *To: *(.*)', string)
        if m:
          attr = None
          overflow = True
          continue
        m = re.search('^ *Cc: (.*)', string)
        if m:
          attr = None
          overflow = True
          continue
        if overflow:
          if string == '<br>':
            overflow = False
          elif attr:
            dict[attr] += ' '+string
          continue
        dict['msg'] += string
    elif msg.get_content_type() == 'image/jpeg':
      images.append('data:image/jpg;base64,'+msg.get_payload())
    elif msg.get_content_type() == 'image/png':
      images.append('data:image/png;base64,'+msg.get_payload())
  return None

data = sys.stdin.read()

msg = email.message_from_string(data)
parse(msg)

if debug:
  print 'From:', dict['sender']
  print 'Date:', dict['date']
  print 'Subject:', dict['subject']
  print 'Message:', dict['msg'][:100]
  sys.exit(0)

dict['images'] = images

dict['subtitle'] = 'Romance Scammer - Beware!'

#print type(dict['msg']), len(dict['msg'])
#print dict['msg'].encode('utf-8')[5872-20:5872+20]

if 'subject' in dict and isinstance(dict['subject'], str):
  dict['subject'] = dict['subject'].decode('utf-8', 'ignore')
if 'msg' in dict and isinstance(dict['msg'], str):
  dict['msg'] = dict['msg'].decode('utf-8', 'ignore')

print RenderY('scammer.html', dict)
