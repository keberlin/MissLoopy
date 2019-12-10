import re

DOMAIN    = r'[a-z0-9][a-z0-9-]+(\.[a-z]{2,5}){1,2}'

EMAIL_REGULAR = r'[a-z0-9][a-z0-9_\.-]*@'+DOMAIN
EMAIL_PATTERN = EMAIL_REGULAR

def MaskEmailAddresses(text):
  if not text:
    return None
  return re.sub(EMAIL_PATTERN, '<blocked email>', text, re.IGNORECASE)

TRANSPORT = r'[a-z]+://'
SITE      = r'([a-z0-9][a-z0-9-]+\.)?'+DOMAIN
PAGE      = r'/[a-z0-9][a-z0-9\.-]*'
patterns = []
patterns.append(TRANSPORT+SITE+'(?:'+PAGE+')*')
patterns.append(SITE+'(?:'+PAGE+')+')
URL_PATTERN = r'|'.join([(pattern) for pattern in patterns])

def MaskUrls(text):
  if not text:
    return None
  return re.sub(URL_PATTERN, '<blocked url>', text, re.IGNORECASE)

patterns = []
patterns.append('(?<=\W)'+SITE+'(?=\W)')
patterns.append('^'+SITE+'(?=\W)')
patterns.append('(?<=\W)'+SITE+'$')
patterns.append('^'+SITE+'$')
SITE_PATTERN = r'|'.join([(pattern) for pattern in patterns])

def MaskSites(text):
  if not text:
    return None
  return re.sub(SITE_PATTERN, '<blocked website>', text, re.IGNORECASE)

TEL_PATTERN = r'[0-9][0-9\- ][0-9\- ][0-9\- ]+[0-9]'

def MaskTelNumbers(text):
  if not text:
    return None
  return re.sub(TEL_PATTERN, '<blocked number>', text, re.IGNORECASE)

def MaskEverything(text):
  if not text:
    return None
  # Convert all <br>s into newlines
  text = re.sub('<br>','\n',text)
  NL = ' \003\003'
  # Convert all newlines into NLs before masking
  text = re.sub(' *[\r\n]+',NL,text)
  text = MaskEmailAddresses(text)
  text = MaskUrls(text)
  text = MaskSites(text)
  text = MaskTelNumbers(text)
  # Convert all NLs back into newlines
  text = re.sub('('+NL+')+','\n',text)
  # Remove any leading newline
  return re.sub('^\n','',text)
