import re

EMAIL_REGULAR = r'([A-Za-z0-9][A-Za-z0-9_.-]*)@([A-Za-z0-9]+)\.([A-Za-z]+(?:\.[A-Za-z]+)*)'

patterns = []

NAME   = '[^ \t\r\n:,]+'
DOMAIN = '[^ \t\r\n:,\.]+'
EXT    = '[^ \t\r\n:,]+'

patterns.append('('+NAME+')@('+DOMAIN+')\.('+EXT+')')

ats = []
ats.append('\W*'.join(['[Aa]+','[Tt]+']))
#ats.append('\W*'.join(['[Oo]','[Ff]']))
ats.append('\W*'.join(['[Oo]','[Nn]']))
AT     = '(?:'+'|'.join([(at) for at in ats])+')'

dots = []
dots.append('\W*'.join(['[Dd]+','[Oo0]+','[Tt]+']))
DOT    = '(?:'+'|'.join([(dot) for dot in dots])+')'

domains = []
domains.append('\W*'.join(['[Gg]','[Mm]','[Aa]','[Ii]','[Ll]']))
domains.append('\W*'.join(['[Yy]','[Aa]','[Hh]','[Oo0Uu]?','[Oo0Uu]?']))
domains.append('\W*'.join(['[Rr]','[Oo]','[Cc]','[Kk]','[Ee]','[Tt]','[Mm]','[Aa]','[Ii]','[Ll]']))
domains.append('\W*'.join(['[Hh]','[Oo]','[Tt]','[Mm]','[Aa]','[Ii]','[Ll]']))
domains.append('\W*'.join(['[Oo]','[Uu]','[Tt]','[Ll]','[Oo]','[Oo]','[Kk]']))
domains.append('\W*'.join(['[Aa]','[Oo]','[Ll]']))
domains.append('\W*'.join(['[Ff]','[Aa]','[Cc]','[Ee]','[Bb]','[Oo]','[Oo]','[Kk]']))
domains.append('\W*'.join(['[Tt]','[Ee]','[Cc]','[Hh]','[Ee]','[Mm]','[Aa]','[Ii]','[Ll]']))
domains.append('\W*'.join(['[Nn]','[Oo]','[Kk]','[Ii]','[Aa]','[Mm]','[Aa]','[Ii]','[Ll]']))
domains.append('\W*'.join(['[Bb]','[Aa]','[Rr]','[Ii]','[Dd]']))
domains.append('\W*'.join(['[Yy]','[Aa]','[Nn]','[Dd]','[Ee]','[Xx]']))
domains.append('\W*'.join(['[Gg]','[Oo]','[Oo]','[Gg]','[Ll]','[Ee]','[Tt]','[Aa]','[Ll]','[Kk]']))
domains.append('\W*'.join(['[Ss]','[Kk]','[Yy]','[Pp]','[Ee]?']))
KNOWN_DOMAIN = '(?:'+'|'.join([(domain) for domain in domains])+')'

exts = []
exts.append('\W*'.join(['[Cc]+','[Oo0]+','[Mm]+']))
exts.append('\W*'.join(['[Cc]','[Oo0]','\.','[Uu]','[Kk]']))
exts.append('\W*'.join(['[Ff]','[Rr]']))
exts.append('\W*'.join(['[Rr]','[Uu]']))
#exts.append('\W*'.join(['[Ii]','[Nn]']))
exts.append('\W*'.join(['[Mm]','[Ee]','[Ss]','[Ss]','[Ee]','[Nn]','[Gg]','[Ee]','[Rr]']))
exts.append('\W*'.join(['[Aa]','[Cc]','[Cc]','[Oo]','[Uu]','[Nn]','[Tt]']))
exts.append('\W*'.join(['[Ii]','[Dd]']))
KNOWN_EXT = '(?:'+'|'.join([(ext) for ext in exts])+')'

patterns.append('('+NAME+')\W*(?:[@#]|'+AT+'\W*)?('+KNOWN_DOMAIN+')(?:\W*(?:\.|'+DOT+'))?(?:\W*('+KNOWN_EXT+'))?')
patterns.append('('+NAME+')\W*[@#]\W*([^@]{1,20})(?:\.|'+DOT+')\W*('+KNOWN_EXT+')')
patterns.append('('+NAME+')\W+'+AT+'\W+([^@]{1,20})(?:\.|'+DOT+')\W*('+KNOWN_EXT+')')

domains = []
domains.append('\W*'.join(['[Yy]','[Mm]','[Aa]','[Ii]','[Ll]']))
domains.append('\W*'.join(['[Ll]','[Ii]','[Vv]','[Ee]']))
domains.append('\W*'.join(['[Ff]','[Bb]']))
domains.append('\W*'.join(['[Yy]','[Mm]']))
LOOSE_DOMAIN = '(?:'+'|'.join([(domain) for domain in domains])+')'

patterns.append('('+NAME+')\W*(?:[@#]|'+AT+'\W*)?('+LOOSE_DOMAIN+')(?:\.|'+DOT+')?\W*('+KNOWN_EXT+')')
patterns.append('('+NAME+')\W*(?:[@#]|'+AT+'\W*)('+LOOSE_DOMAIN+')')

EMAIL_PATTERN = r'|'.join([(pattern) for pattern in patterns])

def MaskEmailAddresses(text):
  if not text:
    return None
  text = re.sub(EMAIL_REGULAR, '<blocked email address>', text)
  return re.sub(EMAIL_PATTERN, '<blocked email address>', text)

TRANSPORT = r'\w+://'
SITE      = r'[\w\.]+\.'+KNOWN_EXT
PAGE      = r'/([\w\.\-]+)?'
patterns = []
patterns.append(TRANSPORT+SITE+'(?:'+PAGE+')*')
patterns.append(SITE+'(?:'+PAGE+')+')
URL_PATTERN = r'|'.join([(pattern) for pattern in patterns])

def MaskUrls(text):
  if not text:
    return None
  return re.sub(URL_PATTERN, '<blocked url>', text)

patterns = []
patterns.append('(?<=\W)'+SITE+'(?=\W)')
patterns.append('^'+SITE+'(?=\W)')
patterns.append('(?<=\W)'+SITE+'$')
patterns.append('^'+SITE+'$')
SITE_PATTERN = r'|'.join([(pattern) for pattern in patterns])

def MaskSites(text):
  return text
  if not text:
    return None
  return re.sub(SITE_PATTERN, '<blocked website>', text)

def MaskEverything(text):
  if not text:
    return None
  # Convert all <br>s into newlines
  text = re.sub('<br>','\n',text)
  NL = ' \003\003'
  # Convert all newlines into NLs before masking
  text = re.sub(' *[\r\n]+',NL,text)
  text = MaskSites(MaskEmailAddresses(MaskUrls(text)))
  # Convert all NLs back into newlines
  text = re.sub('('+NL+')+','\n',text)
  # Remove any leading newline
  return re.sub('^\n','',text)
