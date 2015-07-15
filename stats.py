#!/usr/bin/python

import database

from utils import *
from mlutils import *

def Bit(enum):
  b = 0
  while not enum&(1<<b):
    b += 1
  return b

db = database.Database(MISS_LOOPY_DB)

now = datetime.datetime.utcnow()

total       = 0
unverified  = 0
genders     = [0,0,0,0,0,0]
ages        = [0,0,0,0,0,0]
ethnicities = [0,0,0,0,0,0,0]

db.execute('SELECT * FROM profiles')
for entry in db.fetchall():
  if not entry[COL_VERIFIED]:
    unverified += 1
    continue
  total += 1
  genders[Bit(entry[COL_GENDER])] += 1
  ages[Bit(entry[COL_GENDER])] += Age(entry[COL_DOB])
  ethnicities[Bit(entry[COL_ETHNICITY])] += 1

men   = genders[Bit(GEN_MAN)] + genders[Bit(GEN_SUGAR_PUP)] + genders[Bit(GEN_SUGAR_DADDY)]
women = genders[Bit(GEN_WOMAN)] + genders[Bit(GEN_SUGAR_BABY)] + genders[Bit(GEN_SUGAR_MOMMA)]
ages_men   = ages[Bit(GEN_MAN)] + ages[Bit(GEN_SUGAR_PUP)] + ages[Bit(GEN_SUGAR_DADDY)]
ages_women = ages[Bit(GEN_WOMAN)] + ages[Bit(GEN_SUGAR_BABY)] + ages[Bit(GEN_SUGAR_MOMMA)]

# Get number of active profiles (logged in within the last month)
db.execute('SELECT COUNT(*) FROM profiles WHERE verified AND last_login>=%s' % (Quote(str(now-datetime.timedelta(days=30)))))
entry = db.fetchone()
active = entry[0]

# Get number of sent messages (within the last month)
db.execute('SELECT COUNT(*) FROM emails WHERE sent>=%s' % (Quote(str(now-datetime.timedelta(days=30)))))
entry = db.fetchone()
emails = entry[0]

# Get most blocked members
db.execute('SELECT id_block,COUNT(DISTINCT id) FROM blocked GROUP BY id_block ORDER BY COUNT(DISTINCT id) DESC LIMIT 10')
most_blocked = [(entry[0]) for entry in db.fetchall()]

# Get most favorite members
db.execute('SELECT id_favorite,COUNT(DISTINCT id) FROM favorites GROUP BY id_favorite ORDER BY COUNT(DISTINCT id) DESC LIMIT 10')
most_favorite = [(entry[0]) for entry in db.fetchall()]

print 'Number of verified profiles    : %6d' % (total)
print 'Number of unverified profiles  : %6d' % (unverified)
print 'Number of males                : %6d %4.1f%%' % (men, men*100/float(total))
print 'Number of females              : %6d %4.1f%%' % (women, women*100/float(total))
print 'Number of Men                  : %6d %4.1f%%' % (genders[Bit(GEN_MAN)], genders[Bit(GEN_MAN)]*100/float(total))
print 'Number of Women                : %6d %4.1f%%' % (genders[Bit(GEN_WOMAN)], genders[Bit(GEN_WOMAN)]*100/float(total))
print 'Number of Sugar Pups           : %6d %4.1f%%' % (genders[Bit(GEN_SUGAR_PUP)], genders[Bit(GEN_SUGAR_PUP)]*100/float(total))
print 'Number of Sugar Babies         : %6d %4.1f%%' % (genders[Bit(GEN_SUGAR_BABY)], genders[Bit(GEN_SUGAR_BABY)]*100/float(total))
print 'Number of Sugar Daddies        : %6d %4.1f%%' % (genders[Bit(GEN_SUGAR_DADDY)], genders[Bit(GEN_SUGAR_DADDY)]*100/float(total))
print 'Number of Sugar Mommas         : %6d %4.1f%%' % (genders[Bit(GEN_SUGAR_MOMMA)], genders[Bit(GEN_SUGAR_MOMMA)]*100/float(total))
if men:
  print 'Average age of males           : %6.1f' % (ages_men/float(men))
if women:
  print 'Average age of females         : %6.1f' % (ages_women/float(women))
if genders[Bit(GEN_MAN)]:
  print 'Average age of Men             : %6.1f' % (ages[Bit(GEN_MAN)]/float(genders[Bit(GEN_MAN)]))
if genders[Bit(GEN_WOMAN)]:
  print 'Average age of Women           : %6.1f' % (ages[Bit(GEN_WOMAN)]/float(genders[Bit(GEN_WOMAN)]))
if genders[Bit(GEN_SUGAR_PUP)]:
  print 'Average age of Sugar Pups      : %6.1f' % (ages[Bit(GEN_SUGAR_PUP)]/float(genders[Bit(GEN_SUGAR_PUP)]))
if genders[Bit(GEN_SUGAR_BABY)]:
  print 'Average age of Sugar Babies    : %6.1f' % (ages[Bit(GEN_SUGAR_BABY)]/float(genders[Bit(GEN_SUGAR_BABY)]))
if genders[Bit(GEN_SUGAR_DADDY)]:
  print 'Average age of Sugar Daddies   : %6.1f' % (ages[Bit(GEN_SUGAR_DADDY)]/float(genders[Bit(GEN_SUGAR_DADDY)]))
if genders[Bit(GEN_SUGAR_MOMMA)]:
  print 'Average age of Sugar Mommas    : %6.1f' % (ages[Bit(GEN_SUGAR_MOMMA)]/float(genders[Bit(GEN_SUGAR_MOMMA)]))
if ethnicities[Bit(ETH_WHITE)]:
  print 'Number of White                : %6d %4.1f%%' % (ethnicities[Bit(ETH_WHITE)], ethnicities[Bit(ETH_WHITE)]*100/float(total))
if ethnicities[Bit(ETH_BLACK)]:
  print 'Number of Black                : %6d %4.1f%%' % (ethnicities[Bit(ETH_BLACK)], ethnicities[Bit(ETH_BLACK)]*100/float(total))
if ethnicities[Bit(ETH_LATINO)]:
  print 'Number of Latino               : %6d %4.1f%%' % (ethnicities[Bit(ETH_LATINO)], ethnicities[Bit(ETH_LATINO)]*100/float(total))
if ethnicities[Bit(ETH_INDIAN)]:
  print 'Number of Indian               : %6d %4.1f%%' % (ethnicities[Bit(ETH_INDIAN)], ethnicities[Bit(ETH_INDIAN)]*100/float(total))
if ethnicities[Bit(ETH_ASIAN)]:
  print 'Number of Asian                : %6d %4.1f%%' % (ethnicities[Bit(ETH_ASIAN)], ethnicities[Bit(ETH_ASIAN)]*100/float(total))
if ethnicities[Bit(ETH_MIXED)]:
  print 'Number of Mixed                : %6d %4.1f%%' % (ethnicities[Bit(ETH_MIXED)], ethnicities[Bit(ETH_MIXED)]*100/float(total))
if ethnicities[Bit(ETH_OTHER)]:
  print 'Number of Other                : %6d %4.1f%%' % (ethnicities[Bit(ETH_OTHER)], ethnicities[Bit(ETH_OTHER)]*100/float(total))
print 'Number of active profiles (1m) : %6d %4.1f%%' % (active, active*100/float(total))
print 'Number of messages (1m)        : %6d' % (emails)
print 'Most blocked members           :', most_blocked
print 'Most favorite members          :', most_favorite
