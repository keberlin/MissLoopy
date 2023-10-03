import re


def postcode_safe(postcode):
  return re.sub(' +',' ',postcode.upper().strip())

def postcode_valid(postcode):
  return not re.match('^[A-Z]+[0-9]+( +[0-9]+[A-Z]+)?$',postcode) is None
