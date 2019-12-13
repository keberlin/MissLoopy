import sys, re, database, spam

from mlutils import *

MAX_LENGTH = 100

db = database.Database(MISS_LOOPY_DB)

for arg in sys.argv[1:]:
  id = int(arg)
  density_min = 9999
  spammer = spam.AnalyseSpammer(id)
  db.execute('SELECT DISTINCT message FROM emails WHERE id_from=%d ORDER BY sent' % (id))
  for entry in db.fetchall():
    message = re.sub('[\r\n]+',' ',entry[0])
    tuple = spam.AnalyseSpam(message)
    if spam.IsSpamFactored(tuple, spammer, 2):
      print 'Potential Spam id:%d "%s..." {score:%d, density:%d, hits:%s}' % (id, message.encode('utf-8')[:MAX_LENGTH], tuple[0], tuple[1], tuple[2])
    if tuple[1]:
      density_min = min(density_min,tuple[1])
  print 'id:%d members:%d frequency:%.1f min density:%d' % (id, spammer[0], spammer[1]/float(60*60), density_min)
