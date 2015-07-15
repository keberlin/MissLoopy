import datetime, bisect, re, os, cgi

def Days(month,day):
  return month*31+day

starsigns = ['Aquarius', 'Pices', 'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn']
stardates = [
  Days(1,20),    # Aquarius (January 20th - February 18th)
  Days(2,19),    # Pisces (February 19th - March 20th)
  Days(3,21),    # Aries (March 21st - April 19th)
  Days(4,20),    # Taurus (April 20th - May 20th)
  Days(5,21),    # Gemini (May 21st - June 20th)
  Days(6,21),    # Cancer (June 21st - July 22nd)
  Days(7,23),    # Leo (July 23rd - August 22nd)
  Days(8,23),    # Virgo (August 23rd - September 22nd)
  Days(9,23),    # Libra (September 23rd - October 22nd)
  Days(10,23),   # Scorpio (October 23rd - November 21st)
  Days(11,22),   # Sagittarius (November 22nd - December 21st)
  Days(12,22),   # Capricorn (December 22nd - January 19th)
]

def Starsign(date):
  return starsigns[(bisect.bisect(stardates,Days(date.month,date.day))-1) % len(starsigns)]

def Age(date):
  today = datetime.date.today()
  years = today.year-date.year
  if Days(today.month,today.day) < Days(date.month,date.day):
    years -= 1
  return years

def Text(text,alt=''):
  if text:
    return text
  return alt

def Quote(str):
  return "'" + re.sub(r"'",r"''",str) + "'"

def TimeDiff(td):
  def Format(unit,n):
    return '%d %s%s' % (n, unit, 's' if n > 1 else '')
  if td.days/365:
    return Format('year', td.days/365)
  if td.days/30:
    return Format('month', td.days/30)
  if td.days/7:
    return Format('week', td.days/7)
  if td.days:
    return Format('day', td.days)
  if td.seconds/60/60:
    return Format('hour', td.seconds/60/60)
  if td.seconds/60:
    return Format('minute', td.seconds/60)
  if td.seconds:
    return Format('second', td.seconds)
  return None

def Since(time,recently=True):
  if not time:
    return None
  now = datetime.datetime.utcnow()
  td = now - time
  if recently and td.days == 0 and td.seconds < 60:
    return 'online now'
  return '%s ago' % (TimeDiff(td))

def FetchCookies():
  if not 'HTTP_COOKIE' in os.environ:
    return None
  cookies = {}
  for cookie in os.environ['HTTP_COOKIE'].split(';'):
    s = cookie.strip().split('=')
    if len(s) != 2:
      continue
    cookies[s[0]] = s[1].decode('utf-8','ignore')
  return cookies

def FetchRemoteAddr():
  if not 'REMOTE_ADDR' in os.environ:
    return None
  return os.environ['REMOTE_ADDR']

def FetchFormFields(sep='|'):
  form = cgi.FieldStorage()
  return dict([(field,sep.join(form.getlist(field)).decode('utf-8','ignore')) for field in form.keys()])
