import re

UNIT_CM        = 0
UNIT_M         = 1
UNIT_KM        = 2
UNIT_MILE      = 3
UNIT_FEET      = 4
UNIT_INCH      = 5
UNIT_FEET_INCH = 6

COUNTRIES_FEET_INCHES = ['United States', 'Liberia', 'Myanmar']
COUNTRIES_MILES = ['United States', 'American Samoa', 'United Kingdom', 'Myanmar', 'Bahamas', 'Belize', 'British Virgin Islands', 'Cayman Islands',
                   'Falkland Islands (Malvinas)', 'Dominica', 'Grenada', 'Guam', 'Northern Mariana Islands', 'Samoa', 'Saint Lucia',
                   'Saint Vincent And The Grenadines', 'Ascension And Tristan Da Cunha Saint Helena', 'Saint Kitts And Nevis',
                   'Turks And Caicos Islands', 'U.S. Virgin Islands']

# Return tuple of units for distance and height
def Units(country):
  return (UNIT_MILE if country in COUNTRIES_MILES else UNIT_KM, UNIT_FEET_INCH if country in COUNTRIES_FEET_INCHES else UNIT_M)

# v = UNIT_KM (kilometres)
def Distance(v,units,dec=0):
  if v is None:
    return None
  if units == UNIT_MILE:
    v = v*0.621371192237
    return re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", '%.*f miles' % (dec, v))
  if units == UNIT_M:
    v = v*1000.0
    return re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", '%.*f m' % (dec, v))
  return re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", '%.*f km' % (dec, v))

# v = UNIT_CM (centimetres)
def Height(v,units,dec=0):
  if v is None:
    return None
  if units == UNIT_FEET_INCH:
    v = v/2.54
    return '%d\'%d"' % (v/12, v%12)
  if units == UNIT_M:
    v = v/100.0
    return '%.*fm' % (dec, v)
  return '%.*fcm' % (dec, v)
