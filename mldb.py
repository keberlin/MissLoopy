AGE_MIN = 18
AGE_MAX = 99
HEIGHT_MIN = 120
HEIGHT_MAX = 250

# Columns in profiles
COL_ID               = 0
COL_EMAIL            = 1
COL_PASSWORD         = 2
COL_CREATED_OLD      = 3
COL_VERIFIED         = 4
COL_LAST_LOGIN       = 5
COL_NAME             = 6
COL_GENDER           = 7
COL_DOB              = 8
COL_HEIGHT           = 9
COL_WEIGHT           = 10
COL_ETHNICITY        = 11
COL_EDUCATION        = 12
COL_STATUS           = 13
COL_SMOKING          = 14
COL_DRINKING         = 15
COL_COUNTRY_OLD      = 16
COL_REGION_OLD       = 17
COL_PLACENAME_OLD    = 18
COL_X                = 19
COL_Y                = 20
COL_TZ               = 21
COL_OCCUPATION       = 22
COL_SUMMARY          = 23
COL_DESCRIPTION      = 24
COL_LOOKING_FOR      = 25
COL_GENDER_CHOICE    = 26
COL_AGE_MIN          = 27
COL_AGE_MAX          = 28
COL_HEIGHT_MIN       = 29
COL_HEIGHT_MAX       = 30
COL_WEIGHT_CHOICE    = 31
COL_ETHNICITY_CHOICE = 32
COL_LOCATION         = 33
COL_LAST_IP          = 34
COL_CREATED2         = 35
COL_LAST_IP_COUNTRY  = 36
COL_NOTIFICATIONS    = 37

# Columns in photos
COL3_PID    = 0
COL3_OFFSET = 1
COL3_MASTER = 2

# Columns in emails
COL4_ID_FROM = 0
COL4_ID_TO   = 1
COL4_MESSAGE = 2
COL4_SENT    = 3
COL4_VIEWED  = 4

# Columns in results
COL5_ID          = 0
COL5_ID_SEARCH   = 1
COL5_ID_PREVIOUS = 2
COL5_ID_NEXT     = 3

# Gender enum
GEN_MAN        = 1<<0
GEN_WOMAN      = 1<<1
GEN_SUGAR_PUP   = 1<<2
GEN_SUGAR_BABY  = 1<<3
GEN_SUGAR_DADDY = 1<<4
GEN_SUGAR_MOMMA = 1<<5

# Ethnicity enum
ETH_WHITE  = 1<<0
ETH_BLACK  = 1<<1
ETH_LATINO = 1<<2
ETH_ASIAN  = 1<<3
ETH_MIXED  = 1<<4
ETH_OTHER  = 1<<5
ETH_INDIAN = 1<<6

# Weight enum
WGT_SLIM         = 1<<0
WGT_ATHLETIC     = 1<<1
WGT_AVERAGE      = 1<<2
WGT_EXTRA_POUNDS = 1<<3
WGT_LARGE        = 1<<4

# Education enum
EDU_SCHOOL     = 1<<0
EDU_HIGHER     = 1<<1
EDU_UNIVERSITY = 1<<2

# Status enum
STA_SINGLE       = 1<<0
STA_MARRIED      = 1<<1
STA_COHABITATING = 1<<2
STA_WITH_FRIENDS = 1<<3
STA_WITH_FAMILY  = 1<<4
STA_COMPLICATED  = 1<<5

# Smoking enum
SMO_NEVER   = 1<<0
SMO_SOCIAL  = 1<<1
SMO_REGULAR = 1<<2
SMO_HEAVY   = 1<<3

# Drinking enum
DRI_NEVER   = 1<<0
DRI_SOCIAL  = 1<<1
DRI_REGULAR = 1<<2
DRI_HEAVY   = 1<<3

# Notification enum
NOT_NEW_MEMBERS = 1<<0
NOT_NEW_MESSAGE = 1<<1

PHOTOS_DIR   = 'photos'
MEMBERS_DIR  = 'members'
SCAMMERS_DIR = 'scammers'

def Range(min,max):
  if min and max:
    return 'from %s to %s' % (str(min), str(max))
  if min:
    return 'at least %s' % (str(min))
  if max:
    return 'no more than %s' % (str(max))
  return None

def Gender(enum):
  if not enum:
    return None
  if enum&GEN_MAN:
    return 'Man'
  if enum&GEN_WOMAN:
    return 'Woman'
  if enum&GEN_SUGAR_PUP:
    return 'Sugar Pup'
  if enum&GEN_SUGAR_BABY:
    return 'Sugar Baby'
  if enum&GEN_SUGAR_DADDY:
    return 'Sugar Daddy'
  if enum&GEN_SUGAR_MOMMA:
    return 'Sugar Momma'
  return None

def GenderList(enum):
  if not enum:
    return None
  list = []
  if enum&GEN_MAN:
    list.append('Men')
  if enum&GEN_WOMAN:
    list.append('Women')
  if enum&GEN_SUGAR_PUP:
    list.append('Sugar Pups')
  if enum&GEN_SUGAR_BABY:
    list.append('Sugar Babies')
  if enum&GEN_SUGAR_DADDY:
    list.append('Sugar Daddies')
  if enum&GEN_SUGAR_MOMMA:
    list.append('Sugar Mommas')
  return ' or '.join(list)

def Ethnicity(enum):
  if not enum:
    return None
  if enum&ETH_WHITE:
    return 'White'
  if enum&ETH_BLACK:
    return 'Black'
  if enum&ETH_LATINO:
    return 'Latino'
  if enum&ETH_ASIAN:
    return 'Asian'
  if enum&ETH_MIXED:
    return 'Mixed'
  if enum&ETH_OTHER:
    return 'Other'
  return None

def EthnicityList(enum):
  if not enum:
    return None
  list = []
  if enum&ETH_WHITE:
    list.append('White')
  if enum&ETH_BLACK:
    list.append('Black')
  if enum&ETH_LATINO:
    list.append('Latino')
  if enum&ETH_ASIAN:
    list.append('Asian')
  if enum&ETH_MIXED:
    list.append('Mixed')
  if enum&ETH_OTHER:
    list.append('Other')
  return ' or '.join(list)

def Weight(enum):
  if not enum:
    return None
  if enum&WGT_SLIM:
    return 'Slim'
  if enum&WGT_ATHLETIC:
    return 'Athletic'
  if enum&WGT_AVERAGE:
    return 'Average'
  if enum&WGT_EXTRA_POUNDS:
    return 'A few extra pounds'
  if enum&WGT_LARGE:
    return 'Large'
  return None

def Education(enum):
  if not enum:
    return None
  if enum&EDU_SCHOOL:
    return 'School'
  if enum&EDU_HIGHER:
    return 'College'
  if enum&EDU_UNIVERSITY:
    return 'University'
  return None

def Status(enum):
  if not enum:
    return None
  if enum&STA_SINGLE:
    return 'Single'
  if enum&STA_MARRIED:
    return 'Married'
  if enum&STA_COHABITATING:
    return 'Cohabitating'
  if enum&STA_WITH_FRIENDS:
    return 'With friends'
  if enum&STA_WITH_FAMILY:
    return 'With family'
  if enum&STA_COMPLICATED:
    return 'It\'s complicated'
  return None

def Smoking(enum):
  if not enum:
    return None
  if enum&SMO_NEVER:
    return 'Never'
  if enum&SMO_SOCIAL:
    return 'Social'
  if enum&SMO_REGULAR:
    return 'Regular'
  if enum&SMO_HEAVY:
    return 'Heavy'
  return None

def Drinking(enum):
  if not enum:
    return None
  if enum&DRI_NEVER:
    return 'Never'
  if enum&DRI_SOCIAL:
    return 'Social'
  if enum&DRI_REGULAR:
    return 'Regular'
  if enum&DRI_HEAVY:
    return 'Heavy'
  return None
