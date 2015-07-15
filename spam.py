import re, datetime, time, database

from mlutils import *

def AnalyseSpammer(id):
  db = database.Database(MISS_LOOPY_DB)

  db.execute('SELECT COUNT(DISTINCT id_to),COUNT(*),MIN(sent) FROM emails WHERE id_from=%d' % (id))
  entry = db.fetchone()
  members = entry[0]
  count = entry[1]
  if count == 0:
    return (0, 0)
  sent_min = datetime.datetime(*time.strptime(entry[2],"%Y-%m-%d %H:%M:%S.%f")[:6])
  sent_max = datetime.datetime.utcnow()
  td = sent_max-sent_min
  frequency = (td.days*24*60*60 + td.seconds)/count
  return (members, frequency)

from spamkeywords import *

def AnalyseSpam(text):
  score = 0
  hits = []
  for str,cost in SPAM_KEYWORDS.iteritems():
    matches = re.findall(str, text, re.IGNORECASE)
    if matches:
      score += cost*len(matches)
      hits.append(re.sub(r'[^a-z]+',r' ',str))
  density = len(text)/float(score) if score else 0
  return (score, density, hits)

def IsSpamFactored(tuple,spammer,mult=1):
  # tuple = (score, density, hits)
  # spammer = (members, frequency)
  score     = tuple[0]
  density   = tuple[1]
  members   = spammer[0]
  frequency = spammer[1]
  hours = frequency/(60*60)
  if hours < 1:
    factor = .25
  elif hours < 2:
    factor = .20
  elif hours < 4:
    factor = .15
  elif hours < 6:
    factor = .10
  elif hours < 8:
    factor = .05
  else:
    factor = 0
  density /= 1+factor*members
  return (density and density < 20*mult) or (members >= 25 and hours < 1)
